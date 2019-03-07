from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import *
from online_tests.models import OnlineTest
from recruiters.admin import SuitabilitesInline, JobListingInline
import pdb

# Register your models here.

class PriorEmploymentInline(admin.TabularInline):
	model = PriorEmployment
	can_delete = False
	readonly_fields = ['company','position']
	extra = 0

	def has_add_permission(self,request):
		return False

class DegreeInline(admin.TabularInline):
	model = Degree
	readonly_fields = ['institution','qualification','level_awarded']
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

class SkillHobbyLevelInline(admin.TabularInline):
	model = SkillHobbyLevel
	readonly_fields = []
	can_delete = False
	extra = 0

class OnlineTestInline(admin.StackedInline):
	model=OnlineTest
	readonly_fields = ['application', 'date_completed', 'result', 'link']

	def link(self, obj):
		return format_html(
			'<a href="{l}"><strong>[Click to view]</strong></a>'.format(
				l=reverse('admin:online_tests_onlinetest_change', args=[obj.model_id]),
			)
		)

class JobApplicationInline(admin.StackedInline):
	model = JobApplication
	readonly_fields = ['job_listing','magic_score','test_score','cover_letter','link']
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

@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
	inlines = [
		JobApplicationInline,
		PriorEmploymentInline,
		DegreeInline,
		AlevelInline,
		SkillHobbyLevelInline
	]
	list_display = ('name', 'account')
	readonly_fields = ['account','name','cv','_skills', '_hobbies', '_programming_languages']

	def _base(self, queryset):
		html = "<ul>{}</ul>".format("".join("<li>{}</li>".format(o) for o in queryset))
		return format_html(html)

	def _skills(self, obj):
		return self._base(obj.skills)
	_skills.short_description = 'Skills'

	def _hobbies(self, obj):
		return self._base(obj.hobbies)
	_hobbies.short_description = 'Hobbies'

	def _programming_languages(self, obj):
		return self._base(obj.programming_languages)
	_programming_languages.short_description = 'Programming Languages'

@admin.register(SkillHobby)
class SkillHobbyAdmin(admin.ModelAdmin):
	list_display = ('name', 'kind')

# @admin.register(SkillHobbyLevel)
# class SkillHobbyLevelAdmin(admin.ModelAdmin):
# 	list_display = ('applicant_name', 'skillhobby', 'level')

# 	def applicant_name(self, obj):
# 		return obj.applicant.name

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
	list_display = ('job_listing', 'applicant', 'status', 'last_updated', 'magic_score')
	readonly_fields = ('applicant_profile','_job_listing','date_submitted', 'cover_letter', 'last_updated', 'job_listing')
	exclude = ('applicant','job_listing')

	inlines = [
		SuitabilitesInline,
		OnlineTestInline
	]

	def magic_score(self, obj):
		return "{}%".format(round(obj.application_suitabilities.magic_score * 100,1))

	magic_score.admin_order_field = 'application_suitabilities__magic_score'

	def applicant_profile(self, obj):
		return format_html(
			'<a href="{l}">{a} <strong>[Click to view]</strong></a>'.format(
				l=reverse('admin:applicants_applicantprofile_change', args=[obj.applicant.model_id]),
				a=obj.applicant
			)
		)

	def _job_listing(self, obj):
		return format_html(
			'<a href="{l}">{j} <strong>[Click to view]</strong></a>'.format(
				l=reverse('admin:recruiters_joblisting_change', args=[obj.job_listing.model_id]),
				j=obj.job_listing
			)
		)
	_job_listing.short_description = 'Job listing'

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
	list_display = ('name','department','weight')