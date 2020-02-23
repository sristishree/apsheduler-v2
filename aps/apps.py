from django.apps import AppConfig
from django.conf import settings

class ApsConfig(AppConfig):
    name = 'aps'

    def ready(self):
        from . import scheduler
        print('readyy')
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
