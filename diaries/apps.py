from django.apps import AppConfig

class DiariesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diaries'

    def ready(self):
        import diaries.signals.init_superuser