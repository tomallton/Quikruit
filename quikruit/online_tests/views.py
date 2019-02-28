from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from applicants.models import ApplicantProfile
from .models import *
from django.http import HttpResponseRedirect

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

def prepare(request):
	pass

def test(request):
	pass

def review_test(request):
	pass

def results(request):
	pass