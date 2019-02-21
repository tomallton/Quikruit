from django.contrib import admin
from .models import *

class ReqiredSkillInline(admin.TabularInline):
	model = RequiredSkill

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
	inlines = [
		ReqiredSkillInline,
	]

# Register your models here.
admin.site.register(Department)
admin.site.register(RecruiterProfile)
admin.site.register(RequiredSkill)
admin.site.register(Suitabilities)