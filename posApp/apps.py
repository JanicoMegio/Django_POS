from django.apps import AppConfig


class posAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posApp'

    def ready(self):
        from  .scheduler import scheduler
        scheduler.start()
