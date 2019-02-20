from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import *

# Register your models here.


class PriorEmploymentInline(admin.TabularInline):
	model = PriorEmployment
	can_delete = False
	readonly_fields = ['company','position','employed_from','employed_until']
	extra = 0

	def has_add_permission(self,request):
		return False

class DegreeInline(admin.TabularInline):
	model = Degree
	readonly_fields = ['institution','qualification','date_awarded','level_awarded']
	can_delete = False
	extra = 0

	def has_add_permission(self,request):
		return False

class AlevelInline(admin.TabularInline):
	model = ALevel
	readonly_fields = ['subject','grade']
	can_delete=False
	extra=0

	def has_add_permission(self,request):
		return False

class SkillHobbyInline:
	pass

@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
	inlines = [
		PriorEmploymentInline,
		DegreeInline,
		AlevelInline
	]
	list_display = ('name', 'account')
	readonly_fields = ['account','name','picture','cv']

@admin.register(SkillHobby)
class SkillHobbyAdmin(admin.ModelAdmin):
	list_display = ('name', 'kind')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
	list_display = ('job_listing', 'applicant', 'status', 'last_updated')
	readonly_fields = ('applicant_profile','job_listing','date_submitted', 'cover_letter', 'last_updated')
	exclude = ('applicant',)

	def applicant_profile(self, obj):
		return format_html(
			'<a href="{l}">{a} <strong>[Click to view]</strong></a>'.format(
				l=reverse('admin:applicants_applicantprofile_change', args=[obj.applicant.model_id]),
				a=obj.applicant
			)
		)

admin.site.register(SkillHobbyLevel)