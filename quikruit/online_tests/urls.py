from django.urls import path
from . import views

urlpatterns = [
	path('', views.homepage, name='testing_homepage'),
	path('<slug:test_id>/prepare/', views.prepare, name='testing_prepare'),
	path('<slug:test_id>/test/', views.test, name='testing_test'),
	path('<slug:test_id>/review/', views.review_test, name='testing_review'),
	path('<slug:test_id>/results/', views.results, name='testing_results')
]