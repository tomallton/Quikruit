from django.shortcuts import render

def homepage(request):
	return render(request, 'recruiters/rec_homepage.html', None)

def login(request):
	return render(request, 'recruiters/rec_login.html', None)
