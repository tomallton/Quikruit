from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import *

# Register your models here.


class PriorEmploymentInline(admin.TabularInline):
	model = PriorEmployment
	can_delete = False
	readonly_fields = ['company','position','employment_length']
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
	readonly_fields = ['skillhobby','level']
	extra = 0

@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
	inlines = [
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

	def _hobbies(self, obj):
		return self._base(obj.hobbies)

	def _programming_languages(self, obj):
		return self._base(obj.programming_languages)

@admin.register(SkillHobby)
class SkillHobbyAdmin(admin.ModelAdmin):
	list_display = ('name', 'kind')

@admin.register(SkillHobbyLevel)
class SkillHobbyLevelAdmin(admin.ModelAdmin):
	list_display = ('applicant_name', 'skillhobby', 'level')

	def applicant_name(self, obj):
		return obj.applicant.name

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