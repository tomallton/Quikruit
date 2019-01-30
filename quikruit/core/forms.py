from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model as user 

class AccountCreationForm(forms.ModelForm):
	password = forms.CharField(
		label='Password', 
		widget=forms.PasswordInput()
	)
	password_conf = forms.CharField(
		label='Confirm password', 
		widget=forms.PasswordInput()
	)

	class Meta:
		model = user()
		fields = ('email',)

	def clean_password_conf(self):
		password = self.cleaned_data.get('password')
		password_conf = self.cleaned_data.get('password_conf')
		if password and password_conf and password != password_conf:
			raise forms.ValidationError('Mismatched passwords')
		return password_conf

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

