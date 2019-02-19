from django.urls import path
from . import views

urlpatterns = [
	# Applicants homepage.
	# URL example: http://quikruit.example/applicants/
	path('', views.homepage, name='applicants_homepage'),

	# Applicants login page.
	# URL example: http://quikruit.example/applicants/login/
	path('login/', views.login, name='applicants_login'),

	# Job application page.
	# URL example: http://quikruit.example/applicants/apply/3v4tnf7cgy7yg78/
	path('apply/<slug:job_id>/', views.homepage, name='applicants_apply')
]
