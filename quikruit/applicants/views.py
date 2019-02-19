from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
import pdb
from .models import *
from .forms import *

@login_required(login_url='/applicants/login/')
def homepage(request):
	profile = None
	try:
		profile = request.user.applicant_profile
	except ApplicantProfile.DoesNotExist:
		return HttpResponseRedirect("/Project/applicants/login/")
	context = {
		'profile': profile,
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
   
    profile=request.user.applicant_profile
    error = None
   
    if request.method == "POST":
        
        pdb.set_trace()
        prior_employment_formset = PriorEmploymentFormSet(
            request.POST,
            instance=profile
        )
        if not prior_employment_formset.is_valid():
            error = "Invalid formset"
    elif request.method == "GET":
        a_level_formset = ALevelFormSet(instance=profile)
        prior_employment_formset = PriorEmploymentFormSet(instance=profile)
        degree_formset = DegreeFormSet(instance=profile)
    context = {
        'profile': profile,
        'a_levels': a_level_formset,
        'prior_employment': prior_employment_formset,
        'degree': degree_formset,
        'error': error
    }
    return render(request, 'applicants/app_testformsets.html', context)