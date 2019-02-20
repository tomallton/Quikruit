from django.shortcuts import render
from django.contrib.auth import authenticate
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

def application_form(request):
	return render(request, 'applicants/app_applicationform.html', None)

def test_formset_page(request):
    profile = request.user.applicant_profile
    def render_page():
        a_level_formset = ALevelFormSet(instance=profile)
        prior_employment_formset = PriorEmploymentFormSet(instance=profile)
        degree_formset = DegreeFormSet(instance=profile)
        context = {
            'profile': profile,
            'a_levels': a_level_formset,
            'prior_employment': prior_employment_formset,
            'degree': degree_formset,
        }
        return render(request, 'applicants/app_testformsets.html', context)

    if not request.user.is_applicant:
        return HttpResponseRedirect("/Project/applicants/login/")

   
    if request.method == "POST":
        prior_employment_formset = PriorEmploymentFormSet(
            request.POST,
            instance=profile
        )
        a_level_formset = ALevelFormSet(
            request.POST,
            instance=profile
        )
        degree_formset = DegreeFormSet(
            request.POST,
            instance=profile
        )
        if (not prior_employment_formset.is_valid() or 
            not a_level_formset.is_valid() or
            not degree_formset.is_valid()):
            pdb.set_trace()
        prior_employment_formset.clean()
        prior_employment_formset.save()
        a_level_formset.clean()
        a_level_formset.save() 
        degree_formset.clean()
        degree_formset.save()
        return render_page()
    elif request.method == "GET":
        return render_page()