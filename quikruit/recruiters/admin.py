from django.contrib import admin
from django.urls import reverse
from .models import *
from applicants.models import JobApplication
from core.models import Notification
import pdb

def invite_marked_applications_to_interview(modeladmin, request, queryset):
	for application in queryset:
		application.status = JobApplication.INTERVIEW_REQUESTED
		application.save()

class ReqiredSkillInline(admin.TabularInline):
	model = RequiredSkill

class SuitabilitesInline(admin.TabularInline):
	model = Suitabilities

class JobListingInline(admin.StackedInline):
	model = JobListing
	exclude = ('description','suitable_applications')

class JobApplicationInline(admin.StackedInline):
	model = JobApplication
	readonly_fields = ['applicant','job_listing','magic_score','test_score','cover_letter','link']
	extra = 0

	def magic_score(self, obj):
		return obj.application_suitabilities.magic_score

	def test_score(self, obj):
		# pdb.set_trace()
		return obj.online_test.result

	def link(self, obj):
		return format_html(
			'<a href="{l}"><strong>[Click to view]</strong></a>'.format(
				l=reverse('admin:applicants_jobapplication_change', args=[obj.model_id]),
			)
		)

	def has_add_permission(self,request):
		return False

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
	inlines = [
		ReqiredSkillInline,
		JobApplicationInline
	]
	filter_horizontal = ('suitable_applications',)
	
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		if obj:
			form.base_fields['suitable_applications'].queryset = JobApplication.objects.filter(job_listing=obj)
		else:
			form.base_fields['suitable_applications'].queryset = JobApplication.objects.none()
		return form

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	inlines = [
		JobListingInline,
	]
