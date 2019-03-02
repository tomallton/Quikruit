from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from applicants.models import ApplicantProfile
from .models import *
from django.http import HttpResponseRedirect
from .forms import *

# Create your views here.
def homepage(request):
    try:
        profile = request.user.applicant_profile
    except ApplicantProfile.DoesNotExist:
        return HttpResponseRedirect("/quikruit/applicants/login/")

    context = {
        'profile': profile,
        'tests_requested': OnlineTest.objects.filter(application__applicant=profile)
    }
    return render(request, 'online_tests/testing_homepage.html', context)

def prepare(request, test_id):
    try:
        profile = request.user.applicant_profile
    except ApplicantProfile.DoesNotExist:
        return HttpResponseRedirect("/quikruit/applicants/login/")

    test = OnlineTest.objects.get(pk=test_id)

    context = {
        'profile': profile,
        'test': test
    }
    return render(request, 'online_tests/testing_prepare.html', context)

def test(request, test_id):
    try:
        profile = request.user.applicant_profile
    except ApplicantProfile.DoesNotExist:
        return HttpResponseRedirect("/quikruit/applicants/login/")

    test = OnlineTest.objects.get(pk=test_id)
    response_formset = QuestionResponseFormSet(queryset=QuestionResponse.objects.filter(test=test))

    context = {
        'profile': profile,
        'test': test,
        'response_formset': response_formset
    }

    return render(request, 'online_tests/testing_test.html', context)

def review_test(request):
    pass

def results(request):
    pass