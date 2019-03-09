from django.urls import path
from . import views

urlpatterns = [
	path('<slug:test_id>/prepare/', views.prepare, name='testing_prepare'),
	path('<slug:test_id>/test/', views.test, name='testing_test'),
]