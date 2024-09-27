from django.apps import AppConfig


class PollingappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pollingapp'
    
    def ready(self):
        import pollingapp.signals