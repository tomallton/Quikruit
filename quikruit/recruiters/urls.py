from django.urls import path
from . import views

urlpatterns = [
	# Recruiters homepage, URL example: http://quikruit.example/recruiters/
	path('', views.homepage, name='recruiters_homepage'),

	# Recruiters login page, URL example: http://quikruit.example/recruiters/login/
	path('login/', views.login, name='recruiters_login')
]