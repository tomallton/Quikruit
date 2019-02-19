from django.urls import path
from . import views

urlpatterns = [
	# Applicants homepage.
	# URL example: http://quikruit.example/applicants/
	path('', views.homepage, name='applicants_homepage'),

	# Applicants login page.
	# URL example: http://quikruit.example/applicants/login/
	path('login/', views.login, name='applicants_login'),

	# # Job listing page. 
	# # URL example: http://quikruit.example/job/3v4tnf7cgy7yg78/
	# path('job/<slug:job_id>/', views.homepage, name='applicants_viewjob')

	# Job application form.
	# URL Example: http://quikruit.example/job/3v4tnf7cgy7yg78/apply/
	path('job/apply/', views.application_form, name='applicants_applicationform'),

	path('testing/', views.test_formset_page, name='applicants_testing')
]
