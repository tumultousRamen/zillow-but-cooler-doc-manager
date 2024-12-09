from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documents'
    verbose_name = 'Property Documents'  # How it appears in admin

    def ready(self):
        """
        Override the ready method to perform any necessary initialization.
        For example, connecting signal handlers.
        """
        try:
            import documents.signals  # If you add signals later
        except ImportError:
            pass