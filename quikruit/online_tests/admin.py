from django.contrib import admin
from .models import *
from applicants.models import JobApplication

<<<<<<< Updated upstream
#admin.site.register(OnlineTest)
admin.site.register(TestQuestion)
admin.site.register(QuestionAnswer)
     
class TestQuestionAnswerInLine(admin.TabularInline):
    model = QuestionAnswer
    readonly_fields = ['question','answer','correct']
    
    def question(self,obj):
        return format_html(
			'<a href="{l}">{a} <strong>[Click to view]</strong></a>'.format(
				l=reverse('admin:online_test_TestQuestion_change', args=[obj.testquestion.model_id]),
				a=obj.applicant
			)
        )
    
    def has_delete_permission(self, request, obj=None):
        return False
    extra = 0

@admin.register(OnlineTest)
class OnlineTestAdmin(admin.ModelAdmin):
    inlines = [
        #OnlineTestInline,
        TestQuestionAnswerInLine
    ]
    
    readonly_fields = ['application','date_completed','result']
    list_display = ('application','date_completed','result')
    
    def application(self,obj):
        return format_html(
			'<a href="{l}">{a} <strong>[Click to view]</strong></a>'.format(
				l=reverse('admin:applicants_JobApplication_change', args=[obj.jobapplication.model_id]),
				a=obj.applicant
			)
        )
=======
class QuestionResponseInline(admin.TabularInline):
	model = QuestionResponse
	extra=0
	readonly_fields=['answer', 'correct']

@admin.register(OnlineTest)
class OnlineTestAdmin(admin.ModelAdmin):
	readonly_fields = ['date_completed','result']

	inlines = [
		QuestionResponseInline
	]

admin.site.register(TestQuestion)
>>>>>>> Stashed changes

# Register your models here.
