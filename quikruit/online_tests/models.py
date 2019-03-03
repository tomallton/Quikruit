from django.db import models
from quikruit.mixins import StringBasedModelIDMixin
from markdownx.models import MarkdownxField
import online_tests.fields as custom_fields

class OnlineTest(StringBasedModelIDMixin):
    application = models.ForeignKey(
        'applicants.JobApplication',
        related_name = 'online_test',
        on_delete=models.CASCADE
    )
    
    date_completed  = models.DateTimeField(null=True, blank=True)
    
    result = models.FloatField(null=True, blank=True)

    def __str__(self):
        return 'Test for application: {}'.format(self.application)
    
# class OnlineTestConfig(models.Model):
#     job_listing

class TestQuestion(StringBasedModelIDMixin):
    MULTI_SELECT = 0
    SINGLE_SELECT = 1
    TEXT_ENTRY = 2

    question_type_choices = (
        (MULTI_SELECT, 'Multiple Choice (Checkboxes)'),
        (SINGLE_SELECT,'Multiple Choice (Radio buttons)'),
        # (TEXT_ENTRY, 'Simple text entry')
    )
    answer_count_choices = ((i, i) for i in range(1,6))
    correct_answer_choices = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E')
    )

    question_type = models.IntegerField(choices=question_type_choices)
    
    tested_skill = models.ForeignKey(
        'applicants.SkillHobby',
        related_name = 'question_for_skill',
        on_delete = models.CASCADE,
        null = True
    )

    question = MarkdownxField()
    correct_answer = models.TextField(blank=True)

    def __str__(self):
        return self.question
    
class QuestionResponse(models.Model):
    test = models.ForeignKey(
        'online_tests.OnlineTest',
        related_name = 'question_responses',
        on_delete = models.CASCADE
    )
    
    question = models.ForeignKey(
        'online_tests.TestQuestion',
        related_name = 'questions',
        on_delete = models.CASCADE
    )
    
    answer = models.TextField(blank=True)
    
    @property
    def correct(self):
        return self.answer == self.question.correct_answer

    
# Create your models here.
