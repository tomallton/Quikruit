from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import pdb
from .models import *

@login_required(login_url='/applicants/login/')
def homepage(request):
	profile = None
	try:
		profile = request.user.applicant_profile
	except ApplicantProfile.DoesNotExist:
		return HttpResponseRedirect("/Project/applicants/login/")
	context = {'profile': profile}
	return render(request, 'applicants/app_homepage.html', context)

def login(request):
	return render(request, 'applicants/app_login.html', None)
