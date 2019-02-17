from django.conf.urls import patterns, url
from late_login import views

urlpatterns = [
	# Homepage. URL example: http://quikruit.example/applicants/
	path('', views.homepage, name='applicants_homepage'),

	# Login page. URL example: http://quikruit.example/applicant/login/
	path('login/', views.login, name='applicants_login')
]