# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Addresses(models.Model):
    province = models.ForeignKey('Provinces', models.DO_NOTHING)
    city = models.ForeignKey('Cities', models.DO_NOTHING)
    district = models.ForeignKey('Districts', models.DO_NOTHING)
    village = models.ForeignKey('Villages', models.DO_NOTHING, blank=True, null=True)
    street_address = models.TextField()
    postal_code = models.CharField(max_length=5)
    place_id = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'addresses'


class AttachmentTypes(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'attachment_types'


class Attachments(models.Model):
    messages = models.ForeignKey('Messages', models.DO_NOTHING)
    attachment_type = models.ForeignKey(AttachmentTypes, models.DO_NOTHING)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'attachments'


class AvatarMedias(models.Model):
    media = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'avatar_medias'


class BankTransferFees(models.Model):
    bank = models.ForeignKey('Banks', models.DO_NOTHING)
    amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bank_transfer_fees'


class Banks(models.Model):
    name = models.CharField(unique=True, max_length=150)
    clearing_code = models.CharField(max_length=10)
    media_logo = models.CharField(max_length=255)
    is_deleted = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'banks'


class BannerContents(models.Model):
    banner = models.ForeignKey('Banners', models.DO_NOTHING)
    page_url = models.CharField(max_length=100)
    original_page_url = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'banner_contents'


class BannerLocalizations(models.Model):
    language = models.ForeignKey('Languages', models.DO_NOTHING)
    banner = models.ForeignKey('Banners', models.DO_NOTHING)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'banner_localizations'


class BannerVariant(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'banner_variant'


class Banners(models.Model):
    name = models.CharField(max_length=60)
    media = models.CharField(max_length=100)
    is_active = models.IntegerField()
    orders = models.IntegerField()
    banner_variant_id = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'banners'


class Brands(models.Model):
    manufacturer = models.ForeignKey('Manufacturers', models.DO_NOTHING)
    name = models.CharField(max_length=60)
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'brands'


class CartDetails(models.Model):
    cart = models.ForeignKey('Carts', models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    base_price = models.FloatField()
    discount = models.IntegerField()
    discount_amount = models.FloatField(blank=True, null=True)
    wholesale_discount_amount = models.FloatField()
    final_price = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cart_details'


class CartReferences(models.Model):
    cart = models.ForeignKey('Carts', models.DO_NOTHING)
    influencer_promoted_product = models.ForeignKey('InfluencerPromotedProducts', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cart_references'


class Carts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    unique_code = models.CharField(unique=True, max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'carts'


class ChatUserStatuses(models.Model):
    chat_user = models.ForeignKey('ChatUsers', models.DO_NOTHING)
    online = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'chat_user_statuses'


class ChatUsers(models.Model):
    user_id = models.IntegerField()
    user_type = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'chat_users'


class Cities(models.Model):
    province_id = models.IntegerField()
    name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cities'


class CityCenterPoints(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING)
    center_lat = models.FloatField()
    center_lon = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'city_center_points'


class ClickActions(models.Model):
    value = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'click_actions'


class ComplaintMedias(models.Model):
    complaint = models.ForeignKey('Complaints', models.DO_NOTHING)
    media = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'complaint_medias'


class ComplaintOptionList(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'complaint_option_list'


class ComplaintOptions(models.Model):
    complaint = models.ForeignKey('Complaints', models.DO_NOTHING)
    complaint_option_list = models.ForeignKey(ComplaintOptionList, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'complaint_options'


class ComplaintOrderDetails(models.Model):
    complaint = models.ForeignKey('Complaints', models.DO_NOTHING)
    order_detail = models.ForeignKey('OrderDetails', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'complaint_order_details'


class ComplaintStatuses(models.Model):
    name = models.CharField(max_length=45)
    slug = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'complaint_statuses'


class Complaints(models.Model):
    complaint_type = models.CharField(max_length=45)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    complaint_status = models.ForeignKey(ComplaintStatuses, models.DO_NOTHING)
    reason = models.TextField()
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'complaints'


class Configurations(models.Model):
    key = models.CharField(unique=True, max_length=45)
    value = models.CharField(max_length=255)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'configurations'


class Conversations(models.Model):
    channel_id = models.CharField(unique=True, max_length=45)
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'conversations'


class CuratedOutletStatusHistories(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    current_status = models.ForeignKey('CuratedOutletStatuses', models.DO_NOTHING)
    previous_status = models.ForeignKey('CuratedOutletStatuses', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'curated_outlet_status_histories'


class CuratedOutletStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=120)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'curated_outlet_statuses'


class CuratedOutlets(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'curated_outlets'


class CuratedProductStatusHistories(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    current_status = models.ForeignKey('CuratedProductStatuses', models.DO_NOTHING)
    previous_status = models.ForeignKey('CuratedProductStatuses', models.DO_NOTHING)
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'curated_product_status_histories'


class CuratedProductStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'curated_product_statuses'


class CuratedProducts(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'curated_products'


class DeliveryAreaDetails(models.Model):
    delivery_area = models.ForeignKey('DeliveryAreas', models.DO_NOTHING)
    province = models.ForeignKey('Provinces', models.DO_NOTHING)
    city = models.ForeignKey(Cities, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_area_details'


class DeliveryAreas(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    name = models.CharField(max_length=60)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_areas'


class DeliveryConfirmationExpiry(models.Model):
    order_delivery = models.ForeignKey('OrderDeliveries', models.DO_NOTHING)
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_confirmation_expiry'


class DeliveryPartnerPickupTypes(models.Model):
    delivery_partner = models.ForeignKey('DeliveryPartners', models.DO_NOTHING)
    pickup_type = models.ForeignKey('PickupTypes', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_partner_pickup_types'


class DeliveryPartnerServiceAreas(models.Model):
    delivery_partner_service = models.ForeignKey('DeliveryPartnerServices', models.DO_NOTHING)
    city = models.ForeignKey(Cities, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_partner_service_areas'


class DeliveryPartnerServiceTypes(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_partner_service_types'


class DeliveryPartnerServices(models.Model):
    delivery_partner = models.ForeignKey('DeliveryPartners', models.DO_NOTHING)
    delivery_partner_service_type = models.ForeignKey(DeliveryPartnerServiceTypes, models.DO_NOTHING)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    slug = models.CharField(max_length=60)
    is_active = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    term = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'delivery_partner_services'


class DeliveryPartners(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=45)
    media_logo = models.CharField(max_length=255)
    orders = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_partners'


class DeliveryServiceEtds(models.Model):
    delivery_partner_service = models.ForeignKey(DeliveryPartnerServices, models.DO_NOTHING)
    value = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'delivery_service_etds'


class Districts(models.Model):
    city_id = models.IntegerField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'districts'


class EnrichmentTypes(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'enrichment_types'


class ExternalTempMedia(models.Model):
    product_source_id = models.BigIntegerField(blank=True, null=True)
    media_url = models.TextField(blank=True, null=True)
    media_path = models.TextField(blank=True, null=True)
    id_source = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    update_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'external_temp_media'


class ExternalTempMediaOld(models.Model):
    id_source = models.BigIntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    product_source_id = models.BigIntegerField(blank=True, null=True)
    media_path = models.TextField(blank=True, null=True)
    media_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'external_temp_media_old'


class ExternalTempOutlets(models.Model):
    id_source = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    alias = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tagline = models.TextField(blank=True, null=True)
    active_products = models.IntegerField(blank=True, null=True)
    products_sold = models.IntegerField(blank=True, null=True)
    transaction_count = models.IntegerField(blank=True, null=True)
    favourite_count = models.IntegerField(blank=True, null=True)
    rating_score = models.FloatField(db_column='rating.score', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rating_review_count = models.IntegerField(db_column='rating.review_count', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rating_one_star = models.IntegerField(db_column='rating.one_star', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rating_two_star = models.IntegerField(db_column='rating.two_star', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rating_three_star = models.IntegerField(db_column='rating.three_star', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rating_four_star = models.IntegerField(db_column='rating.four_star', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    rating_five_star = models.IntegerField(db_column='rating.five_star', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    satisfaction_good = models.IntegerField(db_column='satisfaction.good', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    satisfaction_neutral = models.IntegerField(db_column='satisfaction.neutral', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    satisfaction_bad = models.IntegerField(db_column='satisfaction.bad', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    reputation_badge = models.CharField(db_column='reputation.badge', max_length=45, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    reputation_score_level = models.IntegerField(db_column='reputation.score_level', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    reputation_score = models.IntegerField(db_column='reputation.score', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    location = models.CharField(max_length=100, blank=True, null=True)
    is_closed = models.IntegerField(blank=True, null=True)
    response_speed = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=45, blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'external_temp_outlets'


class ExternalTempProducts(models.Model):
    id_source = models.IntegerField(blank=True, null=True)
    outlet_id = models.IntegerField(blank=True, null=True)
    outlet_source_id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    alias = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    strike_price = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)
    menu_name = models.TextField(blank=True, null=True)
    min_order = models.IntegerField(blank=True, null=True)
    max_order = models.IntegerField(blank=True, null=True)
    condition = models.TextField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    main_category = models.TextField(blank=True, null=True)
    sub_category = models.TextField(blank=True, null=True)
    sold = models.IntegerField(blank=True, null=True)
    transactions = models.IntegerField(blank=True, null=True)
    revenue = models.BigIntegerField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    talk_count = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'external_temp_products'


class ExternalTempProductsPareto(models.Model):
    id_source = models.BigIntegerField(blank=True, null=True)
    outlet_id = models.IntegerField(blank=True, null=True)
    outlet_source_id = models.BigIntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    alias = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    strike_price = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)
    menu_name = models.TextField(blank=True, null=True)
    min_order = models.IntegerField(blank=True, null=True)
    max_order = models.IntegerField(blank=True, null=True)
    condition = models.TextField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    main_category = models.TextField(blank=True, null=True)
    sub_category = models.TextField(blank=True, null=True)
    sold = models.IntegerField(blank=True, null=True)
    transactions = models.IntegerField(blank=True, null=True)
    revenue = models.BigIntegerField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    talk_count = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'external_temp_products_pareto'


class FlashSaleProducts(models.Model):
    flash_sale = models.ForeignKey('FlashSales', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_superdeal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'flash_sale_products'


class FlashSales(models.Model):
    is_active = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    campaign_name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'flash_sales'


class ForstokOrders(models.Model):
    forstok_outlet = models.ForeignKey('ForstokOutlets', models.DO_NOTHING)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    forstok_order_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'forstok_orders'


class ForstokOutletProfiles(models.Model):
    forstok_outlet = models.ForeignKey('ForstokOutlets', models.DO_NOTHING)
    profile_name = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'forstok_outlet_profiles'


class ForstokOutlets(models.Model):
    outlet_id = models.IntegerField()
    forstok_account_id = models.PositiveIntegerField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'forstok_outlets'


class ForstokProductCategories(models.Model):
    product_category_id = models.IntegerField()
    forstok_product_category_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'forstok_product_categories'


class ForstokProducts(models.Model):
    forstok_outlet = models.ForeignKey(ForstokOutlets, models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    forstok_product_id = models.IntegerField()
    forstok_product_variant_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'forstok_products'


class ForstokWebhookEvents(models.Model):
    event_name = models.CharField(max_length=255)
    callback_url = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'forstok_webhook_events'


class InfluencerCollectionDetails(models.Model):
    influencer_collection = models.ForeignKey('InfluencerCollections', models.DO_NOTHING)
    influencer_promoted_product = models.ForeignKey('InfluencerPromotedProducts', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencer_collection_details'


class InfluencerCollections(models.Model):
    influencer = models.ForeignKey('Influencers', models.DO_NOTHING)
    name = models.CharField(max_length=60)
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencer_collections'


class InfluencerEarningHistory(models.Model):
    influencer = models.ForeignKey('Influencers', models.DO_NOTHING)
    influencer_promoted_product = models.ForeignKey('InfluencerPromotedProducts', models.DO_NOTHING)
    name = models.CharField(max_length=60)
    quantity_sold = models.IntegerField()
    amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencer_earning_history'


class InfluencerPromotedProductBuyers(models.Model):
    influencer_promoted_product = models.ForeignKey('InfluencerPromotedProducts', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    order_detail = models.ForeignKey('OrderDetails', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencer_promoted_product_buyers'


class InfluencerPromotedProductVisitors(models.Model):
    influencer_promoted_product = models.ForeignKey('InfluencerPromotedProducts', models.DO_NOTHING)
    visitor_uuid = models.CharField(max_length=36)
    user_id = models.IntegerField()
    visited_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencer_promoted_product_visitors'


class InfluencerPromotedProducts(models.Model):
    influencer = models.ForeignKey('Influencers', models.DO_NOTHING)
    outlet_listed_product = models.ForeignKey('OutletListedProducts', models.DO_NOTHING)
    is_active = models.IntegerField()
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencer_promoted_products'


class InfluencerSocialMedias(models.Model):
    influencer = models.ForeignKey('Influencers', models.DO_NOTHING)
    username = models.CharField(max_length=60)
    link = models.CharField(max_length=100)
    followers = models.PositiveIntegerField()
    screenshot = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencer_social_medias'


class InfluencerVisitors(models.Model):
    influencer = models.ForeignKey('Influencers', models.DO_NOTHING)
    visitor_uuid = models.CharField(max_length=36)
    user_id = models.IntegerField()
    visited_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencer_visitors'


class Influencers(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    name = models.CharField(max_length=60)
    slug = models.CharField(unique=True, max_length=60)
    media_avatar = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'influencers'


class InvoiceDetails(models.Model):
    invoice = models.ForeignKey('Invoices', models.DO_NOTHING)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    order_amount = models.FloatField()
    discount_amount = models.FloatField()
    wholesale_discount_amount = models.FloatField()
    promo_amount = models.FloatField()
    delivery_cost = models.FloatField()
    total_amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'invoice_details'


class Invoices(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    ref_no = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'invoices'


class Languages(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'languages'


class Manufacturers(models.Model):
    name = models.CharField(unique=True, max_length=60)
    link = models.CharField(max_length=60)
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'manufacturers'


class MasterProductClusters(models.Model):
    cluster_id = models.IntegerField(blank=True, null=True)
    external_product_id = models.IntegerField(blank=True, null=True)
    product_source_id = models.BigIntegerField(blank=True, null=True)
    internal_product_id = models.IntegerField(blank=True, null=True)
    master_product_id = models.IntegerField(blank=True, null=True)
    master_product_status_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'master_product_clusters'


class MasterProductMedias(models.Model):
    master_product = models.ForeignKey('MasterProducts', models.DO_NOTHING)
    media = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'master_product_medias'


class MasterProductStatusHistories(models.Model):
    master_product_cluster = models.ForeignKey(MasterProductClusters, models.DO_NOTHING)
    previous_status = models.ForeignKey('MasterProductStatuses', models.DO_NOTHING)
    current_status = models.ForeignKey('MasterProductStatuses', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'master_product_status_histories'


class MasterProductStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'master_product_statuses'


class MasterProducts(models.Model):
    brand = models.ForeignKey(Brands, models.DO_NOTHING)
    fin = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=255)
    description = models.TextField()
    product_category_id = models.IntegerField()
    barcode = models.CharField(max_length=255)
    uom = models.CharField(max_length=45)
    weight = models.IntegerField()
    volume = models.IntegerField()
    width = models.FloatField()
    height = models.FloatField()
    length = models.FloatField()
    quantity = models.IntegerField()
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'master_products'


class MeaningfulTopics(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    keyword = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'meaningful_topics'


class MessageStatuses(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'message_statuses'


class Messages(models.Model):
    conversation = models.ForeignKey(Conversations, models.DO_NOTHING)
    sender = models.ForeignKey(ChatUsers, models.DO_NOTHING)
    message_status = models.ForeignKey(MessageStatuses, models.DO_NOTHING)
    body = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'messages'


class Migrations(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    applied_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'migrations'


class MlModels(models.Model):
    name = models.TextField(blank=True, null=True)
    blob = models.TextField(blank=True, null=True)
    in_use = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()
    tag = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ml_models'


class MlProductMatchingSurveys(models.Model):
    ml_product_matching_id = models.IntegerField()
    is_matching = models.SmallIntegerField(blank=True, null=True)
    master_group_id = models.IntegerField(blank=True, null=True)
    additional_group = models.CharField(max_length=60, blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ml_product_matching_surveys'


class MlProductMatchings(models.Model):
    first_product = models.IntegerField(blank=True, null=True)
    second_product = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ml_product_matchings'


class NationalHolidays(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'national_holidays'


class NotificationClickActions(models.Model):
    notification_content = models.ForeignKey('NotificationContents', models.DO_NOTHING)
    click_action = models.ForeignKey(ClickActions, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notification_click_actions'


class NotificationContentLocalizations(models.Model):
    language = models.ForeignKey(Languages, models.DO_NOTHING)
    notification_content = models.ForeignKey('NotificationContents', models.DO_NOTHING)
    title = models.CharField(max_length=60)
    body = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notification_content_localizations'


class NotificationContents(models.Model):
    slug = models.CharField(unique=True, max_length=60)
    title = models.CharField(max_length=60)
    body = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notification_contents'


class OrderCancellationOtherReasons(models.Model):
    order_cancellation = models.ForeignKey('OrderCancellations', models.DO_NOTHING)
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_cancellation_other_reasons'
        unique_together = (('id', 'order_cancellation'),)


class OrderCancellationReasonLocalizations(models.Model):
    language = models.ForeignKey(Languages, models.DO_NOTHING)
    order_cancellation_reason = models.ForeignKey('OrderCancellationReasons', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_cancellation_reason_localizations'


class OrderCancellationReasons(models.Model):
    name = models.CharField(max_length=255)
    orders = models.IntegerField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_cancellation_reasons'


class OrderCancellations(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    order_cancellation_reason = models.ForeignKey(OrderCancellationReasons, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_cancellations'
        unique_together = (('id', 'order', 'order_cancellation_reason'),)


class OrderConfirmationExpiry(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_confirmation_expiry'


class OrderDeliveredConfirmationExpiry(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_delivered_confirmation_expiry'


class OrderDeliveries(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    tracking_number = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_deliveries'


class OrderDeliveryStatusHistories(models.Model):
    order_delivery = models.ForeignKey(OrderDeliveries, models.DO_NOTHING)
    current_status = models.ForeignKey('OrderDeliveryStatuses', models.DO_NOTHING)
    previous_status = models.ForeignKey('OrderDeliveryStatuses', models.DO_NOTHING)
    note = models.CharField(max_length=255)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_delivery_status_histories'


class OrderDeliveryStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_delivery_statuses'


class OrderDetailStatusHistories(models.Model):
    order_detail = models.ForeignKey('OrderDetails', models.DO_NOTHING)
    current_status = models.ForeignKey('OrderDetailStatuses', models.DO_NOTHING)
    previous_status = models.ForeignKey('OrderDetailStatuses', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_detail_status_histories'


class OrderDetailStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_detail_statuses'


class OrderDetails(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    note = models.CharField(max_length=255)
    discount = models.IntegerField()
    discount_amount = models.FloatField()
    wholesale_discount_amount = models.FloatField()
    promo_amount = models.FloatField()
    total_amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_details'


class OrderReviewStatuses(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    status = models.CharField(max_length=14)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_review_statuses'


class OrderStatusHistories(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    current_status = models.ForeignKey('OrderStatuses', models.DO_NOTHING)
    previous_status = models.ForeignKey('OrderStatuses', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_status_histories'


class OrderStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_statuses'


class OrderVouchers(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    voucher = models.ForeignKey('Vouchers', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_vouchers'


class Orders(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    user_address = models.ForeignKey('UserAddresses', models.DO_NOTHING)
    delivery_partner_service = models.ForeignKey(DeliveryPartnerServices, models.DO_NOTHING)
    ref_no = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'orders'


class OutletAdminRoles(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_admin_roles'


class OutletAdmins(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    outlet_admin_role = models.ForeignKey(OutletAdminRoles, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'outlet_admins'


class OutletBannerMedias(models.Model):
    media = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_banner_medias'


class OutletCourierConfigurations(models.Model):
    outlet_courier = models.ForeignKey('OutletCouriers', models.DO_NOTHING)
    outlet_courier_etd = models.ForeignKey('OutletCourierEtds', models.DO_NOTHING)
    is_active = models.IntegerField()
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_flat = models.IntegerField()
    cost = models.FloatField()
    city = models.ForeignKey(Cities, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'outlet_courier_configurations'


class OutletCourierEtds(models.Model):
    slug = models.CharField(max_length=7)
    name = models.CharField(max_length=255)
    second = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_courier_etds'


class OutletCourierProofs(models.Model):
    outlet_courier_configuration = models.ForeignKey(OutletCourierConfigurations, models.DO_NOTHING)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    name = models.CharField(max_length=60)
    media = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_courier_proofs'


class OutletCouriers(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    is_active = models.IntegerField()
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_couriers'


class OutletFees(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    value = models.FloatField()
    unit = models.CharField(max_length=7)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_fees'


class OutletInfluencerMemberships(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    is_registered = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_influencer_memberships'


class OutletListedProducts(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    is_active = models.IntegerField()
    is_deleted = models.IntegerField()
    commission_rate = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_listed_products'


class OutletLocalizations(models.Model):
    language = models.ForeignKey(Languages, models.DO_NOTHING)
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_localizations'


class OutletLocations(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    address = models.ForeignKey(Addresses, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_locations'


class OutletOperationals(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    is_open = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_operationals'


class OutletOwnerMedia(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    id_card = models.CharField(max_length=255)
    id_card_selfie = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_owner_media'


class OutletRatingStatuses(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)
    media_small = models.CharField(max_length=255)
    media_large = models.CharField(max_length=255)
    min_success_order = models.IntegerField()
    min_performance_value = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_rating_statuses'


class OutletRatings(models.Model):
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_ratings'


class OutletScheduleConfigurations(models.Model):
    outlet_schedule = models.ForeignKey('OutletSchedules', models.DO_NOTHING)
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_schedule_configurations'


class OutletSchedules(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    is_national_holiday = models.IntegerField()
    is_outside_schedule = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_schedules'
        unique_together = (('id', 'outlet'),)


class OutletSettlements(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    order_amount = models.FloatField()
    fee = models.FloatField()
    fee_unit = models.CharField(max_length=7)
    total_amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_settlements'


class OutletStatusHistories(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    current_status = models.ForeignKey('OutletStatuses', models.DO_NOTHING, db_column='current_status')
    previous_status = models.ForeignKey('OutletStatuses', models.DO_NOTHING, db_column='previous_status')
    note = models.CharField(max_length=255)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_status_histories'


class OutletStatuses(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_statuses'


class OutletStorefronts(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    name = models.CharField(max_length=60)
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_storefronts'


class OutletSupplierTypes(models.Model):
    supplier_type = models.ForeignKey('SupplierTypes', models.DO_NOTHING)
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_supplier_types'


class OutletTypes(models.Model):
    outlet = models.ForeignKey('Outlets', models.DO_NOTHING)
    type = models.ForeignKey('Types', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'outlet_types'


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


class Pages(models.Model):
    name = models.CharField(max_length=60)
    page_slug = models.CharField(unique=True, max_length=60)
    original_page_url = models.CharField(max_length=100)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pages'


class Participants(models.Model):
    conversation = models.ForeignKey(Conversations, models.DO_NOTHING)
    chat_user = models.ForeignKey(ChatUsers, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'participants'


class PaymentMethodTypes(models.Model):
    name = models.CharField(max_length=60)
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment_method_types'


class PaymentMethods(models.Model):
    payment_method_type = models.ForeignKey(PaymentMethodTypes, models.DO_NOTHING)
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    media_logo = models.CharField(max_length=255)
    convenience_fee = models.FloatField()
    convenience_fee_unit = models.CharField(max_length=7, blank=True, null=True)
    orders = models.IntegerField()
    is_active = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment_methods'


class PaymentPrefixCodes(models.Model):
    payment_method = models.ForeignKey(PaymentMethods, models.DO_NOTHING)
    code = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment_prefix_codes'


class PaymentStatusHistories(models.Model):
    payment = models.ForeignKey('Payments', models.DO_NOTHING)
    current_status = models.ForeignKey('PaymentStatuses', models.DO_NOTHING)
    previous_status = models.ForeignKey('PaymentStatuses', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment_status_histories'


class PaymentStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment_statuses'


class PaymentVirtualAccounts(models.Model):
    payment = models.ForeignKey('Payments', models.DO_NOTHING)
    account_number = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment_virtual_accounts'


class Payments(models.Model):
    invoice = models.ForeignKey(Invoices, models.DO_NOTHING)
    payment_method = models.ForeignKey(PaymentMethods, models.DO_NOTHING)
    payment_amount = models.FloatField()
    wallet_transaction_amount = models.FloatField()
    convenience_fee = models.FloatField()
    total_amount = models.FloatField()
    expired_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payments'


class PickupTypes(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pickup_types'


class PostalCodes(models.Model):
    district = models.ForeignKey(Districts, models.DO_NOTHING)
    value = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'postal_codes'


class ProductCategories(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    media_icon = models.CharField(max_length=255)
    media_banner = models.CharField(max_length=255)
    level = models.IntegerField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_categories'


class ProductCategoryChildren(models.Model):
    product_category_id = models.IntegerField()
    child_category_id = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_category_children'


class ProductCategoryCollections(models.Model):
    product_category_id = models.IntegerField(blank=True, null=True)
    product_collection_group_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_category_collections'


class ProductCategoryLocalizations(models.Model):
    language = models.ForeignKey(Languages, models.DO_NOTHING)
    product_category_id = models.IntegerField()
    name = models.CharField(max_length=255)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_category_localizations'


class ProductCategoryUsages(models.Model):
    product_category_id = models.IntegerField()
    value = models.CharField(max_length=60)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_category_usages'


class ProductCollectionGroups(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_collection_groups'


class ProductDeliveryAreas(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    delivery_area = models.ForeignKey(DeliveryAreas, models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_delivery_areas'


class ProductDeliveryPartners(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    delivery_partner_service = models.ForeignKey(DeliveryPartnerServices, models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_delivery_partners'


class ProductFins(models.Model):
    master_product = models.ForeignKey(MasterProducts, models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    is_removed = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_fins'


class ProductFulfillmentDates(models.Model):
    product_fulfillment = models.ForeignKey('ProductFulfillments', models.DO_NOTHING)
    date = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_fulfillment_dates'


class ProductFulfillmentTypes(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_fulfillment_types'


class ProductFulfillments(models.Model):
    product_fulfillment_type = models.ForeignKey(ProductFulfillmentTypes, models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    interval = models.PositiveIntegerField()
    cut_off_time = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_fulfillments'


class ProductMedias(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    media = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_medias'


class ProductPrices(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    price = models.FloatField()
    min_quantity = models.PositiveIntegerField()
    is_primary = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_prices'


class ProductRecommendations(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    is_recommended = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_recommendations'


class ProductSorting(models.Model):
    label = models.CharField(max_length=45)
    slug = models.CharField(max_length=45)
    is_active = models.IntegerField()
    is_default = models.IntegerField()
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_sorting'


class ProductStrikePriceStatusHistories(models.Model):
    product_strike_price = models.ForeignKey('ProductStrikePrices', models.DO_NOTHING)
    current_status = models.ForeignKey('ProductStrikePriceStatuses', models.DO_NOTHING, db_column='current_status')
    previous_status = models.ForeignKey('ProductStrikePriceStatuses', models.DO_NOTHING, db_column='previous_status')
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_strike_price_status_histories'


class ProductStrikePriceStatuses(models.Model):
    name = models.CharField(max_length=45)
    slug = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_strike_price_statuses'


class ProductStrikePrices(models.Model):
    product = models.ForeignKey('Products', models.DO_NOTHING)
    product_strike_price_status = models.ForeignKey(ProductStrikePriceStatuses, models.DO_NOTHING)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount = models.IntegerField()
    quota = models.IntegerField()
    max_purchase = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_strike_prices'


class ProductTopicHistories(models.Model):
    product_topic_id = models.IntegerField(blank=True, null=True)
    previous_topic_id = models.IntegerField(blank=True, null=True)
    current_topic_id = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_topic_histories'


class ProductTopics(models.Model):
    topic_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    label_name = models.CharField(max_length=45, blank=True, null=True)
    label_id = models.IntegerField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    status_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_topics'


class Products(models.Model):
    outlet = models.ForeignKey(Outlets, models.DO_NOTHING)
    outlet_storefront = models.ForeignKey(OutletStorefronts, models.DO_NOTHING, blank=True, null=True)
    product_category_id = models.IntegerField()
    sku = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.IntegerField()
    stock = models.PositiveIntegerField()
    is_wholesale = models.IntegerField()
    is_active = models.IntegerField()
    is_deleted = models.IntegerField()
    is_bulk = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'products'


class Provinces(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'provinces'


class ReviewContents(models.Model):
    review = models.ForeignKey('Reviews', models.DO_NOTHING)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'review_contents'


class ReviewMedias(models.Model):
    review = models.ForeignKey('Reviews', models.DO_NOTHING)
    media = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'review_medias'


class Reviews(models.Model):
    order_detail_id = models.PositiveIntegerField()
    product_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    reviewer = models.CharField(max_length=255)
    is_anonymous = models.IntegerField()
    rating = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reviews'


class Roles(models.Model):
    value = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'roles'


class ShoppingLists(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shopping_lists'


class SicepatDestinationDistricts(models.Model):
    district = models.ForeignKey(Districts, models.DO_NOTHING)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sicepat_destination_districts'


class SicepatOriginCities(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sicepat_origin_cities'


class SortList(models.Model):
    slug = models.CharField(max_length=60)
    section = models.CharField(max_length=100)
    label = models.CharField(max_length=60)
    is_active = models.IntegerField()
    is_default = models.IntegerField()
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sort_list'


class StrikePricePromotionUsages(models.Model):
    product_strike_price = models.ForeignKey(ProductStrikePrices, models.DO_NOTHING)
    order_detail = models.ForeignKey(OrderDetails, models.DO_NOTHING)
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'strike_price_promotion_usages'


class SupplierTypes(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'supplier_types'


class TopStories(models.Model):
    post_id = models.PositiveIntegerField()
    slug = models.CharField(max_length=255)
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'top_stories'


class TopicLabels(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    renamed = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topic_labels'


class TopicRenames(models.Model):
    topic_correct = models.CharField(max_length=45, blank=True, null=True)
    topic = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topic_renames'


class TopicSourceStatusHistories(models.Model):
    product_topic_id = models.IntegerField(blank=True, null=True)
    previous_status_id = models.IntegerField(blank=True, null=True)
    current_status_id = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topic_source_status_histories'


class TopicSourceStatuses(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=60, blank=True, null=True)
    slug = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topic_source_statuses'


class TopicStatusHistories(models.Model):
    product_topic_id = models.IntegerField(blank=True, null=True)
    previous_status_id = models.IntegerField(blank=True, null=True)
    current_status_id = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topic_status_histories'


class TopicStatuses(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    slug = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topic_statuses'


class Topics(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    renamed = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'topics'


class TypeFeatures(models.Model):
    type = models.ForeignKey('Types', models.DO_NOTHING)
    label = models.CharField(max_length=255)
    is_disable = models.IntegerField()
    feature_type = models.CharField(max_length=7)
    media_logo = models.CharField(max_length=255)
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    caption = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_features'


class Types(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    value = models.FloatField()
    unit = models.CharField(max_length=7)
    media_logo = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'types'


class UserAddresses(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    address = models.ForeignKey(Addresses, models.DO_NOTHING)
    label = models.CharField(max_length=45)
    receiver_name = models.CharField(max_length=255)
    receiver_phone = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    is_primary = models.IntegerField()
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_addresses'


class UserBanks(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    bank = models.ForeignKey(Banks, models.DO_NOTHING)
    account_number = models.CharField(max_length=45)
    account_holder = models.CharField(max_length=45)
    is_deleted = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_banks'


class UserDetails(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    gender = models.CharField(max_length=6, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_details'


class UserFavouriteProducts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_favourite_products'


class UserFcmTokens(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    token = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255)
    device_type = models.CharField(max_length=7)
    app_id = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_fcm_tokens'


class UserRoles(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    created_by = models.PositiveIntegerField()
    updated_by = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_roles'


class UserRooms(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    socket = models.CharField(unique=True, max_length=45)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_rooms'


class Users(models.Model):
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    media_avatar = models.CharField(max_length=255)
    is_active = models.IntegerField()
    language_id = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'


class Villages(models.Model):
    district = models.ForeignKey(Districts, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'villages'


class Villages2(models.Model):
    district = models.ForeignKey(Districts, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'villages2'


class VirtualCategories(models.Model):
    virtual_category_type = models.ForeignKey('VirtualCategoryTypes', models.DO_NOTHING)
    glossary_id = models.IntegerField(blank=True, null=True)
    orders = models.IntegerField()
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=100)
    media_icon = models.CharField(max_length=255)
    media_banner = models.CharField(max_length=255)
    is_active = models.IntegerField()
    is_deleted = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    overline_text = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'virtual_categories'


class VirtualCategoryEnrichments(models.Model):
    virtual_category = models.ForeignKey(VirtualCategories, models.DO_NOTHING)
    enrichment_type = models.ForeignKey(EnrichmentTypes, models.DO_NOTHING)
    enrichment_id = models.IntegerField()
    orders = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'virtual_category_enrichments'


class VirtualCategoryLocalizations(models.Model):
    language = models.ForeignKey(Languages, models.DO_NOTHING)
    virtual_category = models.ForeignKey(VirtualCategories, models.DO_NOTHING)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'virtual_category_localizations'


class VirtualCategoryTypes(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'virtual_category_types'


class VoucherConfigurations(models.Model):
    voucher = models.ForeignKey('Vouchers', models.DO_NOTHING)
    value = models.FloatField()
    value_type = models.CharField(max_length=7)
    max_value = models.FloatField()
    minimum_purchase = models.FloatField()
    target_user = models.CharField(max_length=9)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user_max_usage = models.IntegerField()
    user_max_usage_period = models.CharField(max_length=8)
    quota = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'voucher_configurations'


class VoucherDeductionTypes(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'voucher_deduction_types'


class VoucherEligibleUsers(models.Model):
    voucher = models.ForeignKey('Vouchers', models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'voucher_eligible_users'


class VoucherOutlets(models.Model):
    voucher = models.ForeignKey('Vouchers', models.DO_NOTHING)
    outlet = models.ForeignKey(Outlets, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'voucher_outlets'


class VoucherStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'voucher_statuses'


class VoucherUsages(models.Model):
    voucher = models.ForeignKey('Vouchers', models.DO_NOTHING)
    remaining_quota = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'voucher_usages'


class VoucherUserUsages(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    voucher = models.ForeignKey('Vouchers', models.DO_NOTHING)
    remaining_quota = models.IntegerField()
    last_used_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'voucher_user_usages'


class VoucherUsers(models.Model):
    voucher = models.ForeignKey('Vouchers', models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'voucher_users'


class Vouchers(models.Model):
    voucher_deduction_type = models.ForeignKey(VoucherDeductionTypes, models.DO_NOTHING)
    voucher_status = models.ForeignKey(VoucherStatuses, models.DO_NOTHING)
    name = models.CharField(max_length=60)
    description = models.TextField()
    code = models.CharField(unique=True, max_length=35)
    type = models.CharField(max_length=15)
    issuer = models.CharField(max_length=8)
    outlet_charge_rate = models.FloatField()
    is_active = models.IntegerField()
    is_deleted = models.IntegerField()
    is_public = models.IntegerField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vouchers'


class WalletTransactionLogs(models.Model):
    wallet_transaction = models.ForeignKey('WalletTransactions', models.DO_NOTHING)
    previous_amount = models.FloatField()
    current_amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_transaction_logs'


class WalletTransactionNotes(models.Model):
    wallet_transaction = models.ForeignKey('WalletTransactions', models.DO_NOTHING)
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_transaction_notes'


class WalletTransactionStatusHistories(models.Model):
    wallet_transaction = models.ForeignKey('WalletTransactions', models.DO_NOTHING)
    previous_status = models.ForeignKey('WalletTransactionStatuses', models.DO_NOTHING)
    current_status = models.ForeignKey('WalletTransactionStatuses', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_transaction_status_histories'


class WalletTransactionStatuses(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_transaction_statuses'


class WalletTransactionTypeGroups(models.Model):
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_transaction_type_groups'


class WalletTransactionTypes(models.Model):
    wallet_transaction_type_group = models.ForeignKey(WalletTransactionTypeGroups, models.DO_NOTHING)
    name = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_transaction_types'


class WalletTransactions(models.Model):
    wallet = models.ForeignKey('Wallets', models.DO_NOTHING)
    wallet_transaction_type = models.ForeignKey(WalletTransactionTypes, models.DO_NOTHING)
    ref_no = models.CharField(max_length=45)
    transaction_id = models.IntegerField()
    amount = models.FloatField()
    created_by = models.IntegerField()
    updated_by = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_transactions'


class WalletWithdrawals(models.Model):
    wallet = models.ForeignKey('Wallets', models.DO_NOTHING)
    user_bank = models.ForeignKey(UserBanks, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallet_withdrawals'


class Wallets(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wallets'
