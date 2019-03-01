from django.db import models
from quikruit.mixins import StringBasedModelIDMixin
import online_tests.fields as customFields
from markdownx.models import MarkdownxField

class OnlineTest(StringBasedModelIDMixin):
    application = models.ForeignKey(
        'applicants.JobApplication',
        related_name = 'online_test',
        on_delete=models.CASCADE
    )
    
    date_completed  = models.DateTimeField(null=True, blank=True)
    
    result = models.FloatField(null=True, blank=True)
    
# class OnlineTestConfig(models.Model):
#     job_listing

class TestQuestion(StringBasedModelIDMixin):
    MULTI_SELECT = 0
    SINGLE_SELECT = 1
    TEXT_ENTRY = 2
    ANSWER_LABELS = 4

    question_type_choices = (
        (MULTI_SELECT, 'Multiple Choice (Checkboxes)'),
        (SINGLE_SELECT,'Multiple Choice (Radio buttons)'),
        (TEXT_ENTRY, 'Simple text entry')
    )
    answer_count_choices = ((i, i) for i in range(1,6))
    correct_answer_choices = (
        (0,'A'),
        (1,'B'),
        (2,'C'),
        (3,'D'),
        (4,'E')
    )

    question_type = models.IntegerField(choices=question_type_choices)
    
    tested_skill = models.ForeignKey(
        'applicants.SkillHobby',
        related_name = 'question_for_skill',
        on_delete = models.CASCADE,
        null = True
    )

    question = MarkdownxField()
    answer_count = models.IntegerField(null=True, choices=answer_count_choices)
    correct_answer = models.IntegerField(choices=correct_answer_choices)

    def __str__(self):
        return self.question
    
class QuestionAnswer(models.Model):
    test = models.ForeignKey(
        'online_tests.OnlineTest',
        related_name = 'test_answers',
        on_delete = models.CASCADE
    )
    
    question = models.ForeignKey(
        'online_tests.TestQuestion',
        related_name = 'question_answer',
        on_delete = models.CASCADE
    )
    
    answer = models.TextField(blank=True)
    
    @property
    def correct(self):
        if not self.question.correctAnswer:
            return None
        elif self.answer == self.question.correctAnswer:
            return True
        else:
            return False
    
# Create your models here.
