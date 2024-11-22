# foraging_app/apps.py
from django.apps import AppConfig

class ForagingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foraging_app'

    def ready(self):
        import foraging_app.signals
