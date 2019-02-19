from django import forms
from applicants.models import *

ALevelFormSet = forms.inlineformset_factory(ApplicantProfile, ALevel, extra=1, exclude=[])