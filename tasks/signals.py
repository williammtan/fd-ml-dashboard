from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction

from .models import Session, Train

@receiver(post_save, sender=Session)
def create_or_update_task(sender, instance, created, **kwargs):
    if created:
        task_id = transaction.on_commit(lambda: instance.setup_prodigy_session(), using='ml')

@receiver(pre_save, sender=Train)
def validate_model(sender, instance, **kwargs):
    if instance.model is not None:
        if instance.model.mode != instance.dataset.mode:
            raise Exception('Model\'s mode doesn\'t match with the dataset\'s mode!')
