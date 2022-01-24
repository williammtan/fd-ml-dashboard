# fd-ml-dashboard

Machine Learning Dashboard and API for FOOD.ID

## Setup

### Prerequisites
- [docker](https://docs.docker.com/engine/install/ubuntu/)
- [docker-compose](https://docs.docker.com/compose/install/)

Required files:
- ```.service_account.json``` GCP JSON service account keys (can change path in SERVICE_ACCOUNT_PATH env)
- ```.env``` / ```stage.env``` / ```prod.env``` development/stage/production environment variables (see mock.env)
- ```data/models/sbert.pkl``` pickled file of a sentence_transformer.SentenceTransformer model (use the ```python3 manage.py save_model``` command)
- ```prodigy.json``` prodigy configuration file, fill with database values (see prodigy.mock.json)


### Installation
Clone the git repository
```sh
git clone https://github.com/williammtan/fd-ml-dashboard.git
cd fd-ml-dashboard
```

Pull the git repository
```sh
git pull
```

Switch to the correct branch
```sh
# production
git checkout main

# staging
git checkout develop
```

### Run
Create the .env file (change the values)
```sh
cp mock.env .env
vi .env # change some variables
```

Test docker-compose locally
```sh
docker-compose up -d --build # -d for running in the background, --build to build the images
```

Stop docker-compose
```sh
docker-compose down
```

Push and trigger github actions deployment
```sh
git push
```

