from django import forms
from applicants.models import *

ALevelFormSet = forms.inlineformset_factory(ApplicantProfile, ALevel, extra=0, exclude=[])
DegreeFormSet = forms.inlineformset_factory(ApplicantProfile, Degree, extra=0, exclude=[])
PriorEmploymentFormSet = forms.inlineformset_factory(ApplicantProfile, PriorEmployment, extra=1, exclude=[])