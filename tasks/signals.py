from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from .models import Session

@receiver(post_save, sender=Session)
def create_or_update_task(sender, instance, created, **kwargs):
    if created:
        task_id = transaction.on_commit(lambda: instance.setup_prodigy_session(), using='ml')
