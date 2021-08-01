from django.apps import AppConfig


class SummaryConfig(AppConfig):
    name = 'summary'

    # Starts the scheduler
    # https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6    
    def ready(self):
        from alpaca_service import updater
        updater.start()
