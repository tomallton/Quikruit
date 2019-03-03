from django import forms
from .models import *
import pdb

class QuestionResponseForm(forms.ModelForm):
	radio_choice = forms.ChoiceField(
		choices=(('A','A'),('B','B'),('C','C'),('D','D'),('E','E')),
		widget=forms.RadioSelect,
		required=False
	)

	multiple_choice = forms.MultipleChoiceField(
		choices=(('A','A'),('B','B'),('C','C'),('D','D'),('E','E')),
		widget=forms.CheckboxSelectMultiple,
		required=False
	)

	class Meta:
		model=QuestionResponse
		fields=['question']

	def save(self, commit=True):
		instance = super(QuestionResponseForm, self).save(commit=False)
		if not instance.answer:
			if instance.question.question_type == TestQuestion.SINGLE_SELECT:
				instance.answer = self.cleaned_data['radio_choice']
			elif instance.question.question_type == TestQuestion.MULTI_SELECT:
				instance.answer = ''.join(char for char in self.cleaned_data['multiple_choice'])
		if commit:
			instance.save()
		return instance

QuestionResponseFormSet = forms.modelformset_factory(QuestionResponse, form=QuestionResponseForm, extra=0)