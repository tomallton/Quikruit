from django import forms
from .models import *

class QuestionResponseForm(forms.ModelForm):
	radio_choice = forms.ChoiceField(
		choices=((0,'A'),(1,'B'),(2,'C'),(3,'D'),(4,'E')),
		widget=forms.RadioSelect
	)

	multiple_choice = forms.MultipleChoiceField(
		choices=((0,'A'),(1,'B'),(2,'C'),(3,'D'),(4,'E')),
		widget=forms.CheckboxSelectMultiple
	)

	class Meta:
		model=QuestionResponse
		fields=['question']

QuestionResponseFormSet = forms.modelformset_factory(QuestionResponse, form=QuestionResponseForm, extra=0)