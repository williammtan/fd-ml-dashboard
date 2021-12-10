from django.db import models
from django.urls import reverse

from collection.models import Product

class BooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return int(value) # return 0/1

class Topic(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    renamed = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def products(self):
        return Product.objects.filter(producttopic__topic=self)
    
    def get_absolute_url(self):
        return reverse('topics:index')

    class Meta:
        managed = False
        db_table = 'topics'

class Label(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    renamed = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'topic_labels'

class TopicStatus(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    slug = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def to_dict(cls):
        """Create a slug: status mapping"""
        statuses = cls.objects.all()
        return {s.slug: s for s in statuses}

    class Meta:
        managed = False
        db_table = 'topic_statuses'

class TopicSourceStatus(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=60, blank=True, null=True)
    slug = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def to_dict(cls):
        """Create a slug: status mapping"""
        statuses = cls.objects.all()
        return {s.slug: s for s in statuses}

    class Meta:
        managed = False
        db_table = 'topic_source_statuses'

class ProductTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(TopicStatus, on_delete=models.DO_NOTHING)
    source = models.ForeignKey(TopicSourceStatus, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'product_topics'

class TopicSourceStatusHistory(models.Model):
    product_topic = models.ForeignKey(ProductTopic, on_delete=models.DO_NOTHING)
    previous_status = models.ForeignKey(TopicSourceStatus, on_delete=models.DO_NOTHING, related_name='previous_source')
    current_status = models.ForeignKey(TopicSourceStatus, on_delete=models.DO_NOTHING, related_name='related_source')
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'topic_source_status_histories'

class TopicStatusHistory(models.Model):
    product_topic = models.ForeignKey(ProductTopic, on_delete=models.DO_NOTHING)
    previous_status = models.ForeignKey(TopicStatus, on_delete=models.DO_NOTHING, related_name='previous_status')
    current_status = models.ForeignKey(TopicStatus, on_delete=models.DO_NOTHING, related_name='current_status')
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'topic_status_histories'
