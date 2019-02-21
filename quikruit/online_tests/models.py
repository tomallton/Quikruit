from django.db import models
from quikruit.mixins import StringBasedModelIDMixin

class OnlineTest(StringBasedModelIDMixin):
    application = models.ForeignKey(
        'applicantsJobApplication',
        related_name = 'online_test',
        on_delete=models.CASCADE
    )
    
    dateCompleted  = models.DateTimeField(null=True, blank=True)
    
    result = models.FloatField(null=True, blank=True)
    
class TestQuestion(StringBasedModelIDMixin):
    questionType = models.IntegerField() #TODO: decide on the types
    
    testSkill = models.ForeignKey(
        'applicants.skill',
        related_name = 'question_for_skill',
        on_delete = models.CASCADE,
        null = True
    )
    
    question = models.TextField()
    
    answers = models.TextField(blank=True)
    
    correctAnswer = models.TextField(blank=True)
    
class QuestionAnswer(models.Model):
    test = models.ForeignKey(
        'online_tests.OnlineTest',
        related_name = 'test_answers',
        on_delete = models.CASCADE
    )
    
    question = models.ForeignKey(
        'online_test.TestQuestion',
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
