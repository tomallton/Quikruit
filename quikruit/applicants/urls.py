from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	# Applicants homepage.
	# URL example: http://quikruit.example/applicants/
	path('', views.homepage, name='applicants_homepage'),

	# Applicants login page.
	# URL example: http://quikruit.example/applicants/login/
	path('login/', auth_views.LoginView.as_view(template_name='applicants/app_login.html'), name='applicants_login'),

	path('logout/', auth_views.LogoutView.as_view(template_name='applicants/app_logout.html'), name='applicants_logout'),

	# # Job listing page. 
	# # URL example: http://quikruit.example/job/3v4tnf7cgy7yg78/
	# path('job/<slug:job_id>/', views.homepage, name='applicants_viewjob')

	# Job application form.
	# URL Example: http://quikruit.example/job/3v4tnf7cgy7yg78/apply/
	path('job/apply/', views.application_form, name='applicants_applicationform'),

	path('register/', views.register, name='applicants_registration')
]
