from django.contrib import admin
from .models import *
from applicants.models import JobApplication
from django.utils.html import format_html
from django.urls import reverse

admin.site.register(TestQuestion)
     
class TestQuestionResponseInLine(admin.TabularInline):
    model = QuestionResponse
    fields = ['question','answer','correct']
    readonly_fields = ['_question','answer','correct']
    
    def _question(self,obj):
        return format_html(
            '<a href="{l}">{a} <strong>[Click to view]</strong></a>'.format(
                l=reverse('admin:online_tests_testquestion_change', args=[obj.question.model_id]),
                a='{}...'.format(obj.question.question[:100])
            )
        )
    
    def has_delete_permission(self, request, obj=None):
        return False
    extra = 0

@admin.register(OnlineTest)
class OnlineTestAdmin(admin.ModelAdmin):
    inlines = [
        #OnlineTestInline,
        TestQuestionResponseInLine
    ]
    
    fields = ['_Application','date_completed','result']
    readonly_fields = ['_Application','date_completed','result']
    list_display = ('applicant','job_listing','date_completed','result')
    
    def applicant(self, obj):
        return obj.application.applicant

    def job_listing(self, obj):
        return obj.application.job_listing

    def _Application(self,obj):
        return format_html(
            '<a href="{l}">{a} <strong>[Click to view]</strong></a>'.format(
                l=reverse('admin:applicants_jobapplication_change', args=[obj.application.model_id]),
                a=obj.application
            )
        )
# Register your models here.
