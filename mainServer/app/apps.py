from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = "sample app"

    def ready(self):
        """
        This function is called when startup.
        """
        print("updating start.")
        from .search import start
        start()