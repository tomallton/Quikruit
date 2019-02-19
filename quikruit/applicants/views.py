from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
import pdb
from .models import *
from .forms import ALevelFormSet

@login_required(login_url='/applicants/login/')
def homepage(request):
	if not request.user.is_applicant:
		return HttpResponseRedirect("/Project/applicants/login/")
	context = {
		'profile': request.user.applicant_profile,
		'current_date_and_time': timezone.now()
	}
	return render(request, 'applicants/app_homepage.html', context)

def login(request):
	return render(request, 'applicants/app_login.html', None)

def application_form(request):
	return render(request, 'applicants/app_applicationform.html', None)

def test_formset_page(request):
	if not request.user.is_applicant:
		return HttpResponseRedirect("/Project/applicants/login/")
	context = {
		'profile': request.user.applicant_profile,
		'a_levels': ALevelFormSet(instance=request.user.applicant_profile)
	}
	return render(request, 'applicants/app_testformsets.html', context)