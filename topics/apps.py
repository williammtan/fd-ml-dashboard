from django.apps import AppConfig


class TopicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'topics'

    def ready(self):
        from topics import signals
