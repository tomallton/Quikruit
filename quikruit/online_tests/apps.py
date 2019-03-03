from django.apps import AppConfig

class OnlineTestsConfig(AppConfig):
    name = 'online_tests'

    def ready(self):
    	import online_tests.signals.handlers
    	print('signals imported for online_tests')
