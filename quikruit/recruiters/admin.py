from django.contrib import admin
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
	exclude = ('description',)

class JobApplicationInline(admin.StackedInline):
	model = JobApplication
	readonly_fields = ['applicant', 'cover_letter']
	extra = 0

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
			form.base_fields['suitable_applications'].queryset = None
		return form

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	inlines = [
		JobListingInline,
	]

# Register your models here.
admin.site.register(RequiredSkill)