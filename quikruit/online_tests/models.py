from django.db import models
from django.utils.html import format_html
from quikruit.mixins import StringBasedModelIDMixin
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from applicants.models import SkillHobby
from recruiters.models import RequiredSkill
import random

class OnlineTest(StringBasedModelIDMixin):
    application = models.OneToOneField(
        'applicants.JobApplication',
        related_name = 'online_test',
        on_delete=models.CASCADE
    )
    
    date_completed  = models.DateTimeField(null=True, blank=True)
    
    result = models.FloatField(null=True, blank=True)

    def assign_questions(self, test_questions):
        if test_questions is None:
            return
        for q in test_questions:
            response = QuestionResponse()
            response.test = self
            response.question = q
            response.save()

    def populate(self):
        job_listing = self.application.job_listing
        application = self.application.applicant
        for required_skill_obj in job_listing.required_skills.all():
            required_skill = required_skill_obj.skill
            if required_skill_obj.priority == RequiredSkill.MUST:
                self.assign_questions(questions_for_skill(required_skill, 3))
            elif required_skill_obj.priority == RequiredSkill.SHOULD:
                self.assign_questions(questions_for_skill(required_skill, 1))
            elif (required_skill_obj.priority == RequiredSkill.COULD 
                and random.random() > 0.5):
                self.assign_questions(questions_for_skill(required_skill, 1))

        for skill_level in self.application.applicant.skill_hobby_levels.exclude(skillhobby__kind=SkillHobby.HOBBY):
            probability_of_asking = skill_level.level / 10
            if random.random() > probability_of_asking:
                self.assign_questions(questions_for_skill(skill_level.skillhobby, 1))

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

    @property
    def html_question(self):
        return format_html(markdownify(self.question))

    def __str__(self):
        return self.question
    
def questions_for_skill(skill, count):
    try: 
        return random.sample(list(TestQuestion.objects.filter(tested_skill=skill)), count)
    except ValueError:
        questions = TestQuestion.objects.filter(tested_skill=skill)

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
