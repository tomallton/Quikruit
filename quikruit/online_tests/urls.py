from django.urls import path
from . import views

urlpatterns = [
	path('', views.homepage, name='testing_homepage'),
	path('<slug:testid>/prepare/', views.preface, name='testing_preface'),
	path('<slig:testid>/test/' views.test, name='testing_test'),
	path('<slug:testid>/review/', views.review_test, name='testing_review'),
	path('<slug:testid>/results/', views.results, name='testing_results')
]