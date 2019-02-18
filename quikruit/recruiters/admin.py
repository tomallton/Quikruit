from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(RecruiterProfile)
admin.site.register(JobListing)
admin.site.register(RequiredSkill)
admin.site.register(Suitabilities)