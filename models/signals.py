from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Train

@receiver(pre_save, sender=Train)
def validate_model(sender, instance, **kwargs):
    if instance.model is not None:
        if instance.model.mode != instance.dataset.mode:
            raise Exception('Model\'s mode doesn\'t match with the dataset\'s mode!')
