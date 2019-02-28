from django.db import models
from quikruit.mixins import StringBasedModelIDMixin
from markdownx.models import MarkdownxField
from django import template
from markdownx.utils import markdownify

register = template.Library()

@register.filter
def show_markdown(text):
    return markdownify(text)

class Department(models.Model):
    name = models.CharField(
        max_length=40,
        primary_key=True
    )

    def __str__(self):
        return self.name

class RecruiterProfile(models.Model):
    account = models.OneToOneField(
        'core.QuikruitAccount',
        related_name="recruiter_profile",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=40)

    department = models.ForeignKey(
        'recruiters.Department',
        related_name = "recruiters",
        on_delete=models.CASCADE
    )
    picture = models.ImageField(null=True)

class JobListing(StringBasedModelIDMixin):
    title = models.CharField(max_length=40)
    description = MarkdownxField()
    department = models.ForeignKey(
        'recruiters.Department',
        related_name='job_listings',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{0}: {1}".format(self.department, self.title)

class RequiredSkill(models.Model):
    job_listing = models.ForeignKey(
        'recruiters.JobListing',
        related_name ='required_skills',
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        'applicants.SkillHobby',
        related_name='required_skills',
        on_delete=models.CASCADE
    )

    MUST = 2
    SHOULD = 1
    COULD = 0

    PRIORITY_CHOICES = (
        (MUST,  "Need to have"),
        (SHOULD, "Should have"),
        (COULD, "Nice to have")
    )

    priority = models.IntegerField(
        choices=PRIORITY_CHOICES
    )

    def __str__(self):
        return "{} requires".format(self.job_listing)

class Suitabilities(models.Model):
    application = models.ForeignKey(
        'applicants.JobApplication',
        related_name = 'application_suitabilities',
        on_delete=models.CASCADE
    )
    magic_score = models.FloatField()
    specific_score = models.FloatField()
