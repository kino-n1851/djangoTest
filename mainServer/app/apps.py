from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = "MLapp"

    def ready(self):
        print("updating start.")
        
        from .search import Searcher
        searcher = Searcher()
        searcher.start()