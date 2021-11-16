from django.db import models
from django.db.models import Count
from labeling.models import Dataset

class OutletStorefronts(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    name = models.CharField(max_length=60)
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_storefronts'

class Outlets(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    media_logo = models.CharField(max_length=255)
    media_banner = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlets'

class Product(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    outlet_storefront = models.ForeignKey('OutletStorefronts', models.DO_NOTHING, blank=True, null=True)
    product_category = models.ForeignKey('ProductCategory', models.DO_NOTHING)
    sku = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.IntegerField()
    stock = models.PositiveIntegerField()
    is_wholesale = models.IntegerField()
    is_active = models.IntegerField()
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'products'

class ProductCategory(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    media_icon = models.CharField(max_length=255)
    media_banner = models.CharField(max_length=255)
    level = models.IntegerField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'product_categories'
    
    def __str__(self):
        return self.name

class ProductCategoryChildren(models.Model):
    product_category = models.ForeignKey(ProductCategory, models.DO_NOTHING)
    child_category = models.ForeignKey(ProductCategory, models.DO_NOTHING, related_name='child')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'product_category_children'

class Collection(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    categories = models.ManyToManyField(
        ProductCategory,
        through='ProductCategoryCollection'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'product_collection_groups'
        ordering = ['name']
    
    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return str(self.id)
    
    def dataset_choice(self):
        return Dataset.objects.filter(collection=self.id)
    
    def product_choice(self):
        return Product.objects.filter(product_category__child__product_category__collection=self)
    
    def product_count(self):
        """Get the number of products in the collection"""
        return self.categories.aggregate(product_count=Count('product'))['product_count']

class ProductCategoryCollection(models.Model):
    product_category = models.ForeignKey(ProductCategory, models.CASCADE)
    product_collection_group = models.ForeignKey(Collection, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'product_category_collections'
