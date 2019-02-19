from django.contrib import admin
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

class ApplicantProfileAdmin(admin.ModelAdmin):
	inlines = [
		PriorEmploymentInline,
		DegreeInline,
		AlevelInline
	]

class SkillHobbyAdmin(admin.ModelAdmin):
	list_display = ('name', 'kind')

admin.site.register(ApplicantProfile, ApplicantProfileAdmin)
admin.site.register(JobApplication)
admin.site.register(SkillHobby, SkillHobbyAdmin)
admin.site.register(SkillHobbyLevel)