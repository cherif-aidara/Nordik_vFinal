from django.apps import AppConfig


class ClientsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clients"
    verbose_name = "Gestion de la relation client"
    
    def ready(self):
        """Charger les signaux lors du démarrage de l'application."""
        import clients.signals  # noqa


