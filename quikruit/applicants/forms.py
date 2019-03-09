from django import forms
from applicants.models import *
import pdb

class SkillHobbyLevelForm(forms.ModelForm):
	skill_hobby = forms.CharField(widget=forms.TextInput(attrs={'class':'skillhobbyslot'}))
	skill_hobby.label = 'Skill / Hobby / Programming Language'

	level = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step': '1', 'min':'0', 'max':'10'}))

	def __init__(self, *args, **kwargs):
		super(SkillHobbyLevelForm, self).__init__(*args, **kwargs)
		try:
			self.fields['skill_hobby'].initial = self.instance.skillhobby.name
			self.fields['skill_hobby'].widget.attrs = {'class': 'skillhobbyslot filled'}
		except SkillHobbyLevel.skillhobby.RelatedObjectDoesNotExist:
			pass

	def save(self, commit=True):
		instance = super(SkillHobbyLevelForm, self).save(commit=False)
		if self.cleaned_data['id'] is None:
			try:
				sh = SkillHobby.objects.get(name=self.cleaned_data['skill_hobby'])
			except SkillHobby.DoesNotExist:
				sh = SkillHobby()
				sh.name = self.cleaned_data['skill_hobby']
				sh.kind = SkillHobby.UNCATEGORISED
				sh.save()
			instance.skillhobby = sh
		if commit:
			instance.save()
		return instance

	class Meta:
		model = SkillHobbyLevel
		fields = ('skill_hobby', 'level', 'id')

class ApplicantProfileForm(forms.ModelForm):
	class Meta:
		model = ApplicantProfile
		fields = ('name','picture')

class JobApplicationForm(forms.ModelForm):
	class Meta:
		model = JobApplication
		fields = ('cover_letter',)

ALevelFormSet = forms.inlineformset_factory(ApplicantProfile, ALevel, extra=0, exclude=[], can_delete=False)
DegreeFormSet = forms.inlineformset_factory(ApplicantProfile, Degree, extra=0, exclude=[], can_delete=False)
PriorEmploymentFormSet = forms.inlineformset_factory(ApplicantProfile, PriorEmployment, extra=0, exclude=[], can_delete=False)
SkillHobbyLevelFormSet = forms.inlineformset_factory(ApplicantProfile, SkillHobbyLevel, form=SkillHobbyLevelForm, extra=0, can_delete=False)