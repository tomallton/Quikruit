from django.shortcuts import render

def homepage(request):
	return render(request, 'recruiters/homepage_employer.html', None)

def login(request):
	return render(request, 'recruiters/login_employer.html', None)