from django.apps import AppConfig


class AsiacarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asiacar'

    def ready(self):  # for periodic tasks on the db
        from databaseUpdater import updater 
        updater.start()