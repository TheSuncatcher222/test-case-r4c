from django.apps import AppConfig
from django.db.models.signals import post_save


class CustomersConfig(AppConfig):
    name = 'customers'

    def ready(self):
        from .signals import robot_post_save_handler

        post_save.connect(
            receiver=robot_post_save_handler,
            dispatch_uid="path.to.this.module"
        )
