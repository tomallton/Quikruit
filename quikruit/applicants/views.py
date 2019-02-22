from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
import pdb
from .models import *
from .forms import *
from core.forms import AccountCreationForm

@login_required(login_url='/applicants/login/')
def homepage(request):
	profile = None
	try:
		profile = request.user.applicant_profile
	except ApplicantProfile.DoesNotExist:
		return HttpResponseRedirect("/Project/applicants/login/")
	context = {
		'profile': profile,
        'notifications': profile.account.notifications.all(),
		'current_date_and_time': timezone.now()
	}
	return render(request, 'applicants/app_homepage.html', context)

def register(request):
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('applicants_homepage'))

    if request.method == 'POST':
        account_form = AccountCreationForm(request.POST)
        profile_form = ApplicantProfileForm(request.POST)
        
        if account_form.errors or profile_form.errors:
            context = {
                'account_form': account_form,
                'profile_form': profile_form,
                'account_errors': account_form.errors,
                'profile_errors': profile_form.errors,
            }
        else:
            account_form.instance.is_active = True
            new_account = account_form.save()
            profile_form.instance.account = new_account
            profile_form.save()
            return HttpResponseRedirect(reverse('applicants_homepage'))
    else:
        account_form = AccountCreationForm()
        profile_form = ApplicantProfileForm()
        # pdb.set_trace()
        context = {
            'account_form': account_form,
            'profile_form': profile_form
        }
    return render(request, 'applicants/app_registration.html', context)

def application_form(request):
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
        return render(request, 'applicants/app_applicationform.html', context)

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
