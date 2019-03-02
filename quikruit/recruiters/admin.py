from django.contrib import admin
from .models import *
from applicants.models import JobApplication

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

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	inlines = [
		JobListingInline,
	]

# Register your models here.
admin.site.register(RequiredSkill)