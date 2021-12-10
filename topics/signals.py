from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProductTopic, TopicSourceStatusHistory, TopicStatusHistory

@receiver(post_save, sender=ProductTopic)
def add_status_histories(sender, instance, created, **kwargs):
    if created:
        status_history = TopicStatusHistory(
            product_topic=instance,
            previous_status=instance.status,
            current_status=instance.status,
        )
        status_history.save()
        source_history = TopicSourceStatusHistory(
            product_topic=instance,
            previous_status=instance.source,
            current_status=instance.source,
        )
        source_history.save()
