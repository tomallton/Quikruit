from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from applicants.models import ApplicantProfile
from .models import *
from applicants.models import JobApplication
from django.http import HttpResponseRedirect
from .forms import *
import pdb
from django.utils import timezone as tz

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

    if request.method == 'POST':
        response_formset = QuestionResponseFormSet(request.POST)
        response_formset.save()
        answers = test.question_responses.all()
        correct_answers = [a for a in answers if a.correct]
        score = (len(correct_answers) / len(answers))
        test.result = score
        test.date_completed = tz.now()
        test.save()
        application = test.application
        application.status = JobApplication.ONLINE_TEST_COMPLETED
        application.save()
        return render(request, 'online_tests/testing_complete.html', None)

    if test.date_completed is not None:
        return render(request, 'online_tests/testing_complete.html', None)

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