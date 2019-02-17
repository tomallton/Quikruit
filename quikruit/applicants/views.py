from django.shortcuts import render

def homepage(request):
	return render(request, 'applicants/homepage_applicant.html', None)

def login(request):
	return render(request, 'applicants/login_applicant.html', None)