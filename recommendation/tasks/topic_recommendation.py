from celery import shared_task
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import itertools
from google.cloud import bigquery
from google.oauth2 import service_account
from django.conf import settings
from django.db import connections, transaction
from django.db import close_old_connections
from pymongo import MongoClient

from ..models import TopicRecommendation

credentials = service_account.Credentials.from_service_account_file(
    settings.SERVICE_ACCOUNT_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
bqclient = bigquery.Client(credentials=credentials, project=credentials.project_id,)

conn = MongoClient(settings.MONGO_URI)['foodid-prod']

DEFAULT_EVENT_WEIGHTS = {
    'view_item': 1,
    'add_to_cart': 4,
    'view_cart': 1,
    'remove_from_cart': 0,
    'begin_checkout': 5,
    'add_payment_info': 0,
    'purchase': 10,
    'add_to_wishlist': 4
}

DEFAULT_LABEL_WEIGHTS = {
    'dish': 4,
    'ingredient': 1,
    'ingredients': 1,
    'variant': 3,
    'size': 0,
    'name': 4,
    'brand': 3,
    'meat': 2,
    'weight': 0,
    'origin': 2,
    'vitamin': 0,
    'plantingmedium': 0,
    'relevant': 0,
    'protein type': 1,
    None: 0
}

def get_user_interaction(weights=DEFAULT_EVENT_WEIGHTS):
    """Get user interactions
    Args:
        weights - dict containing {event_name: weight} (defaults to DEFAULT_EVENT_WEIGHTS). Set None to make all weights 1

    Returns:
        user_interactions - pd.DataFrame with columns user_id, item_id, rating
        user_interactions_sparse - sparse.csr_matrix with num_users x num_items, filled with ratings
        user_id_mapping - dict containing {user_idx: user_id}
        item_id_mapping - dict containing {item_idx: item_id}
    """
    query = """
    SELECT
        user_id,
        i.item_id AS item_id,
        event_name,
        FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S',TIMESTAMP_MICROS(event_timestamp)) as timestamp,
    FROM (
        SELECT
            *,
            (
            SELECT
            value.string_value
            FROM
            UNNEST(event_params)
            WHERE
            key = "service") AS service
        FROM
            `analytics_229779991.events_*`
        ),
    UNNEST(items) AS i
    WHERE
        user_id IS NOT NULL
        AND i.item_id IS NOT NULL
        AND i.item_id != "(not set)"
    """
    user_interactions = bqclient.query(query).result().to_dataframe()
    user_interactions['user_id'] = user_interactions['user_id'].astype(int)
    user_interactions['item_id'] = user_interactions['item_id'].astype(int)

    user_ids_c = user_interactions.user_id.astype('category')
    user_id_mapping = dict(enumerate(user_ids_c.cat.categories))
    user_interactions['user_id'] = user_ids_c.cat.codes

    item_ids_c = user_interactions.item_id.astype('category')
    item_id_mapping = dict(enumerate(item_ids_c.cat.categories))
    user_interactions['item_id'] = item_ids_c.cat.codes

    if weights:
        event_weights = {e: 1 for e in user_interactions['event_name'].unique()}
        event_weights.update(weights)

        user_interactions['rating'] = user_interactions['event_name'].apply(lambda x: event_weights[x])
        user_interactions = user_interactions[['user_id', 'item_id', 'rating']]
        user_interactions_sparse = user_interactions.groupby(['user_id', 'item_id']).sum().reset_index()
    else:
        user_interactions['rating'] = 1
        user_interactions = user_interactions[['user_id', 'item_id', 'rating']]
        user_interactions_sparse = user_interactions.groupby(['user_id', 'item_id']).sum().reset_index()
    
    user_interactions_sparse = sparse.csr_matrix((user_interactions_sparse['rating'], (user_interactions_sparse['user_id'], user_interactions_sparse['item_id'])), shape=(len(user_id_mapping), len(item_id_mapping)))

    return user_interactions, user_interactions_sparse, user_id_mapping, item_id_mapping

def get_product_topics(item_id_mapping, min_count=5, sbert_model='paraphrase-multilingual-MiniLM-L12-v2', weights=DEFAULT_LABEL_WEIGHTS):
    """Generate a product x topic matrix with the help of a sbert model
    Args:
        item_id_mapping - mapping for items to use
        min_count - minumum number of topic occurences
        sbert_model - input to sentence_transformers.SentenceTransformer() (defaults to 'paraphrase-multilingual-MiniLM-L12-v2')
        weights - dict for label weights, {label: weight} (defaults to DEFAULT_LABEL_WEIGHTS). Set None to make all weights 1
    
    Returns:
        product_topic_similarity - sparse.csr_matrix of num_items x num_topics
        product_topics - pd.DataFrame with columns product_id, topic_id, label_name, similarity
        topics - pd.DataFrame with columns id, name, idx, embedding

    """
    product_topic_query = f"""
    SELECT product_topics.product_id, product_topics.topic_id, LOWER(topic_labels.name) as label_name
    FROM product_topics
    JOIN topic_labels ON product_topics.label_id = topic_labels.id
    WHERE product_topics.topic_id IN(
        SELECT product_topics.topic_id
        FROM product_topics
        GROUP BY product_topics.topic_id
        HAVING COUNT(product_topics.topic_id) > {min_count}
    )
    AND product_topics.source_id != 4 AND product_topics.source_id != 2
    """ # ignore classification for now

    topic_query = f"""
    SELECT topics.id, TRIM(topics.name) as name
    FROM product_topics
    JOIN topics ON product_topics.topic_id = topics.id
    GROUP BY topics.id, topics.name
    HAVING COUNT(topics.id) > {min_count} 
    """

    products_query = "SELECT * FROM products"

    product_topics = pd.read_sql(product_topic_query, connections['food'])
    topics = pd.read_sql(topic_query, connections['food'])
    products = pd.read_sql(products_query, connections['food'])

    item_id_mapping_inv = {int(v):k for k,v in item_id_mapping.items()}
    product_topics['product_id'] = product_topics['product_id'].map(item_id_mapping_inv)
    product_topics = product_topics.dropna()
    product_topics['product_id'] = product_topics['product_id'].astype(int)
    products['idx'] = products.id.map(item_id_mapping_inv)

    topics = topics[topics.id.isin(product_topics.topic_id)]
    product_topics = product_topics[product_topics.topic_id.isin(topics.id)]

    topic_ids_c = topics.id.astype('category')
    topic_id_mapping = dict(enumerate(topic_ids_c.cat.categories))
    topic_id_mapping_inv = {int(v):k for k,v in topic_id_mapping.items()}
    topics['idx'] = topic_ids_c.cat.codes
    product_topics['topic_id'] = product_topics['topic_id'].map(topic_id_mapping_inv)

    label_weights = {l: 1 for l in product_topics['label_name']}
    label_weights.update(weights)

    # sbert
    sbert = SentenceTransformer(sbert_model)
    topics['embedding'] = list(sbert.encode(topics.name.tolist()))

    product_topic_similarity = np.zeros((len(item_id_mapping),len(topic_id_mapping)))

    for pid, pt in tqdm(product_topics.merge(topics, left_on='topic_id', right_on='idx', how='left').groupby('product_id')):
        product_name = products[products.idx == pid].iloc[0]['name']
        pt['weight'] = cosine_similarity(np.stack(pt['embedding'].values, axis=0), sbert.encode([product_name])).reshape(-1)
        pt['weight'] = pt.apply(lambda x: label_weights[x.label_name] * x.weight, axis=1)
        product_topic_similarity[pid, pt.topic_id] = pt['weight']

    return sparse.csr_matrix(product_topic_similarity), product_topics, topics

def get_user_search(topics, user_id_mapping, log=3):
    """Queries the MongoDB database for user queries
    Args:
        topics - pd.DataFrame with columns id, name, idx, embedding (output from get_product_topics())
        user_id_mapping - mapping for users to use
        log - log base for no. hits (defaults to 3)

    Returns:
        user_search - pd.DataFrame with columns _id, user_id (user index), key (preprocessed with lower() and strip()), hits, created_at, updated_at
        keywords - pd.DataFrame with columns id (generated from index), key, hits, weight (log2 weight from no. hits), topics (list of topics ids found in the keyword)
    """
    cursor = conn['user_recent_search'].find()
    user_search = pd.DataFrame(list(cursor))
    user_search['key'] = user_search['key'].str.lower()
    user_search['key'] = user_search['key'].str.strip()
    user_search['user_id'] = user_search['user_id'].map({v:k for k,v in user_id_mapping.items()})
    user_search = user_search.dropna()
    user_search['user_id'] = user_search['user_id'].astype(int)

    topic_clean = topics[topics.name.str.len() > 2]

    keywords = user_search[['key', 'hits',]].groupby(['key']).sum().sort_values(by='hits', ascending=False).reset_index()
    keywords['topics'] = keywords.key.apply(lambda x: [id for id, name in zip(topic_clean.idx, topic_clean.name) if name in x])
    keywords = keywords[keywords.topics.apply(lambda x: len(x) != 0)].reset_index(drop=True)
    keywords['id'] = keywords.index
    keywords['weight'] = np.log(keywords['hits']) / np.log(3)

    return user_search, keywords

@shared_task(bind=True)
def topic_recommendation_search(self, num_recommendations=10, min_count=5, max_same_topics=3, alpha=3): # alpha is a hyperparameter associated with the log weight of keyword hits
    self.update_state(state='PROGRESS')
    user_interactions, user_interactions_sparse, user_id_mapping, item_id_mapping = get_user_interaction()
    product_topic_sparse, product_topics, topics = get_product_topics(item_id_mapping=item_id_mapping, min_count=min_count)
    user_topic_interactions = np.matmul(user_interactions_sparse.toarray(), product_topic_sparse.toarray())
    user_search, keywords = get_user_search(topics, user_id_mapping, log=alpha)

    topic_keyword_sparse = sparse.csr_matrix((len(topics), len(keywords)))
    for id, k in keywords.iterrows():
        for t in k.topics:
            topic_keyword_sparse[t, id] = k.weight
    
    for i, search in user_search.merge(keywords, on='key').iterrows():
        for t in search.topics:
            user_topic_interactions[search.user_id, t] += search.weight * search.hits_x # add additional weight from user's search
    
    user_keyword_sparse = np.matmul(user_topic_interactions, topic_keyword_sparse.toarray())

    def recommend(user_idx, top_k=10, max_same_topics=3):
    
        keywords['user_pred'] = user_keyword_sparse[user_idx]
        preds = keywords[keywords['user_pred'] > 0].sort_values(by='user_pred', ascending=False)

        keys = []
        counter = {}
        for _, p in preds.iterrows():
            skip = False
            for t in p.topics:
                if counter.get(t, 0) > max_same_topics:
                    skip = True
            
            if not skip:
                for t in p.topics:
                    counter[t] = counter.get(t, 0) + 1 # increment counter
                
                keys.append([p.key, p.user_pred])
        
        return keys[:top_k]
    
    recommendations = pd.DataFrame([
        {
            'user_id': user_id,
            'keyword': rec[0],
            'prob': rec[1]
        }
        for user_id in tqdm(range(len(user_id_mapping)))
        for rec in recommend(user_id, num_recommendations, max_same_topics)
    ])

    min_max_scaler = MinMaxScaler()
    for user_id, recs in recommendations.groupby('user_id'):
        recs['prob'] = min_max_scaler.fit_transform(recs['prob'].values.reshape(-1, 1))
        for i, r in recs.iterrows():
            recommendations.loc[i, 'prob'] = r['prob']
    
    recommendations['user_id'] = recommendations['user_id'].map(user_id_mapping)

    close_old_connections()
    with transaction.atomic(using='food'):
        TopicRecommendation.objects.all().delete()

        topic_recommendations = [
            TopicRecommendation(user_id=row['user_id'], keyword=row['keyword'], confidence=row['prob'])
            for i, row in recommendations.iterrows()
        ]
        recs = TopicRecommendation.objects.bulk_create(topic_recommendations)


@shared_task(bind=True)
def topic_recommendation(self, num_recommendations=10, num_bigram=4, min_count=5):
    self.update_state(state='PROGRESS')
    products = pd.read_sql('SELECT id, name, description FROM products', connections['food'])
    
    def recommend(user_idx, k=10):
        recs = user_topic_interactions[user_idx].argsort()[::-1][:k]

        keywords = []
        for idx in recs:
            topic = topics[topics.idx == idx].iloc[0]
            if user_topic_interactions[user_idx][idx] != 0:
                keywords.append([topic['name'], user_topic_interactions[user_idx][idx]])

        return keywords

    user_interactions, user_interactions_sparse, user_id_mapping, item_id_mapping = get_user_interaction()
    product_topic_sparse, product_topics, topics = get_product_topics(item_id_mapping=item_id_mapping, min_count=min_count)
    user_topic_interactions = np.matmul(user_interactions_sparse.toarray(), product_topic_sparse.toarray())

    recommendations = pd.DataFrame([
        {
            'user_id': user_id,
            'keyword': rec[0],
            'prob': rec[1]
        }
        for user_id in tqdm(range(len(user_id_mapping)))
        for rec in recommend(user_id, 10)
    ])

    min_max_scaler = MinMaxScaler()

    for user_id, recs in recommendations.groupby('user_id'):
        recs['prob'] = min_max_scaler.fit_transform(recs['prob'].values.reshape(-1, 1))
        for i, r in recs.iterrows():
            recommendations.loc[i, 'prob'] = r['prob']

    # bigram topics

    def unique(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    
    keyword_dict = {}

    def recommend_bigram(user_idx, top_k=30):
        product_ids = user_interactions[user_interactions.user_id==user_idx].item_id

        combs = list(itertools.chain.from_iterable(itertools.combinations(pt.topic_id, 2) for pid, pt in product_topics[product_topics.product_id.isin(product_ids)].groupby('product_id')))
        weights = list(
            itertools.chain.from_iterable(
                [
                    product_topic_sparse[pid, t1] * product_topic_sparse[pid, t2] for t1, t2
                    in itertools.combinations(pt.topic_id, 2)
                ] 
                for pid, pt in product_topics[product_topics.product_id.isin(product_ids)].groupby('product_id')))

        user_cooccurrence = np.zeros((len(topics), len(topics))).astype('float64')
        if len(combs) > 0:
            np.add.at(user_cooccurrence, tuple(np.array(combs).T), weights)
            np.add.at(user_cooccurrence, tuple([np.array(combs).T[1], np.array(combs).T[0]]), weights)
        np.fill_diagonal(user_cooccurrence, 0)

        element_wise = np.multiply(topic_bigrams, user_cooccurrence)
        indices = np.array(np.unravel_index(element_wise.ravel().argsort()[::-1][:top_k], element_wise.shape))
        indices.sort(axis=0)
        indices, ind = np.unique(indices.T, axis=0, return_index=True)
        indices = indices[np.argsort(ind)]
        
        done = []
        final = []
        for i1, i2 in indices:
            if i1 not in done and i2 not in done and max([element_wise[i1, i2], element_wise[i2, i1]]) != 0 and cooccurrence[i1, i2] > 2:
                final.append([i1, i2])
                done.extend([i1, i2])
        
        keywords = []
        for i in final:
            i.sort()
            key = ','.join(map(str, i))
            if key not in keyword_dict:
                name = topics[topics.idx.isin(i)].name.tolist()
                name.reverse()
                probs = [len(products[(products.name + ' ' + products.description).str.contains(name[0] + ' ' + name[1])]), len(products[(products.name + ' ' + products.description).str.contains(name[1] + ' ' + name[0])])]
                if probs[0] != probs[1]: # for topic ordering
                    name = name[np.argmax(probs)] + ' ' + name[np.argmin(probs)]
                else:
                    name = ' '.join(name)
                
                name = ' '.join(unique(name.split()))
                keyword_dict[key] = name
            else:
                name = keyword_dict[key]
            keywords.append([name, max([element_wise[i[0], i[1]], element_wise[i[1], i[0]]])])

        return keywords

    cooccurrence = np.zeros((product_topics.topic_id.max()+1,product_topics.topic_id.max()+1))

    for pid, pt in tqdm(product_topics.merge(topics, left_on='topic_id', right_on='idx', how='left').groupby('product_id')):
        comb = list(itertools.combinations(pt.topic_id.tolist(), 2)) # combinations of topics 
        weights = [product_topic_sparse[pid, t1] * product_topic_sparse[pid, t2] for t1, t2 in comb] # weights for each combination
        if len(comb) > 0:
            np.add.at(cooccurrence, tuple(np.array(comb).T), weights)
            np.add.at(cooccurrence, tuple([np.array(comb).T[1], np.array(comb).T[0]]), weights)

    topic_counts = np.zeros(cooccurrence.shape[0])
    for tid, count in product_topics.topic_id.value_counts().iteritems():
        topic_counts[tid] = count
        
    topic_bigrams = cooccurrence / topic_counts # normalize by count of topics

    recommendations_bigram = pd.DataFrame([
        {
            'user_id': user_id,
            'keyword': rec[0],
            'prob': rec[1]
        }
        for user_id in tqdm(range(len(user_id_mapping)))
        for rec in recommend_bigram(user_id, 100)
    ])

    min_max_scaler = MinMaxScaler()
    for user_id, recs in recommendations_bigram.groupby('user_id'):
        recs['prob'] = min_max_scaler.fit_transform(recs['prob'].values.reshape(-1, 1))
        for i, r in recs.iterrows():
            recommendations_bigram.loc[i, 'prob'] = r['prob']
    
    final_recommendations = recommendations.groupby('user_id').head(num_recommendations-num_bigram).append(recommendations_bigram.groupby('user_id').head(num_bigram)).drop_duplicates(subset=['user_id', 'keyword'])
    final_recommendations['user_id'] = final_recommendations['user_id'].map(user_id_mapping)

    close_old_connections()
    with transaction.atomic(using='food'):
        TopicRecommendation.objects.all().delete()

        topic_recommendations = [
            TopicRecommendation(user_id=row['user_id'], keyword=row['keyword'], confidence=row['prob'])
            for i, row in final_recommendations.iterrows()
        ]
        recs = TopicRecommendation.objects.bulk_create(topic_recommendations)
