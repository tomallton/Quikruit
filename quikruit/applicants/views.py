from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
import pdb
from .models import *
from .forms import *
from recruiters.models import JobListing
from core.forms import AccountCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

@login_required(login_url='/quikruit/applicants/login/')
def homepage(request):
	profile = None
	try:
		profile = request.user.applicant_profile
	except ApplicantProfile.DoesNotExist:
		return HttpResponseRedirect("/quikruit/applicants/login/")
	context = {
		'profile': profile,
        'notifications': profile.account.notifications.order_by('-created'),
		'current_date_and_time': timezone.now(),
        'job_listings': JobListing.objects.all()
	}
	return render(request, 'applicants/app_homepage.html', context)

def register(request):
    context = {}
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('applicants_homepage'))

    if request.method == 'POST':
        account_form = AccountCreationForm(request.POST)
        profile_form = ApplicantProfileForm(request.POST, request.FILES)

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
            login(request, new_account)
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

# @login_required(login_url='/quikruit/applicants/login/')
# def application_form(request, job_id):
#     try:
#         profile = request.user.applicant_profile
#     except ApplicantProfile.DoesNotExist:
#         return HttpResponseRedirect("/quikruit/applicants/login/")
#     context = {
#         'profile': profile,
#         'job': JobListing.objects.get(pk=job_id)
#     }
#     return render(request, 'applicants/app_applicationform.html', context)

@login_required(login_url='/quikruit/applicants/login/')
def application_form(request, job_id):
    try:
        profile = request.user.applicant_profile
    except ApplicantProfile.DoesNotExist:
        return HttpResponseRedirect("/quikruit/applicants/login/")
    job = JobListing.objects.get(pk=job_id)
    def render_page():
        a_level_formset = ALevelFormSet(instance=profile)
        prior_employment_formset = PriorEmploymentFormSet(instance=profile)
        degree_formset = DegreeFormSet(instance=profile)
        cover_letter_form = JobApplicationForm()
        skills_and_hobbies_formset = SkillHobbyLevelFormSet(instance=profile)
        context = {
            'job': job,
            'profile': profile,
            'a_levels': a_level_formset,
            'prior_employment': prior_employment_formset,
            'skills_and_hobbies': skills_and_hobbies_formset,
            'cover_letter_form': cover_letter_form,
            'degree': degree_formset,
        }
        return render(request, 'applicants/app_applicationform.html', context)

    if not request.user.is_applicant:
        return HttpResponseRedirect("/quikruit/applicants/login/")


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
        skills_and_hobbies_formset = SkillHobbyLevelFormSet(
            request.POST,
            instance=profile
        )
        job_application_form = JobApplicationForm(
            request.POST
        )
        job_application_form.instance.applicant = profile
        job_application_form.instance.job_listing = job

        if (not prior_employment_formset.is_valid() or
            not a_level_formset.is_valid() or
            not degree_formset.is_valid() or
            not skills_and_hobbies_formset.is_valid() or
            not job_application_form.is_valid()):
            context = {
                'job': job,
                'profile': profile,
                'a_levels': a_level_formset,
                'prior_employment': prior_employment_formset,
                'skills_and_hobbies': skills_and_hobbies_formset,
                'cover_letter_form': job_application_form,
                'degree': degree_formset,
            }
            return render(request, 'applicants/app_applicationform.html', context)
        prior_employment_formset.clean()
        prior_employment_formset.save()
        a_level_formset.clean()
        a_level_formset.save()
        degree_formset.clean()
        degree_formset.save()
        skills_and_hobbies_formset.clean()
        skills_and_hobbies_formset.save()
        job_application_form.clean()
        job_application_form.save()
        return HttpResponseRedirect(reverse('applicants_homepage'))
    elif request.method == "GET":
        return render_page()

@login_required(login_url='/quikruit/applicants/login/')
def job_list(request):
    profile = None
    try:
        profile = request.user.applicant_profile
    except ApplicantProfile.DoesNotExist:
        return HttpResponseRedirect("/quikruit/applicants/login/")
    context = {
        'profile': profile,
        'job_listings': JobListing.objects.all()
    }
    return render(request, 'applicants/app_joblistings.html', context)

@login_required(login_url='/quikruit/applicants/login/')
def settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'applicants/app_homepage.html', {
        'form': form
    })
