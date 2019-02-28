from django import forms
from applicants.models import *

ALevelFormSet = forms.inlineformset_factory(ApplicantProfile, ALevel, extra=0, exclude=[])
DegreeFormSet = forms.inlineformset_factory(ApplicantProfile, Degree, extra=0, exclude=[])
PriorEmploymentFormSet = forms.inlineformset_factory(ApplicantProfile, PriorEmployment, extra=0, exclude=[])
SkillHobbyLevelFormSet = forms.inlineformset_factory(ApplicantProfile, SkillHobbyLevel, extra=0, exclude=[])

class ApplicantProfileForm(forms.ModelForm):
	class Meta:
		model = ApplicantProfile
		fields = ('name','picture')

class JobApplicationForm(forms.ModelForm):
	class Meta:
		model = JobApplication
		fields = ('cover_letter',)