from django.apps import AppConfig

class ApplicantsConfig(AppConfig):
    name = 'applicants'

    def ready(self):
    	import applicants.signals.handlers
    	print("applicants: signals imported.")