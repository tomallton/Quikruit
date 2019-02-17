from django.db import models
from quikruit.mixins import StringBasedModelIDMixin

class Department(models.Model):
	name = models.CharField(
		max_length=40, 
		primary_key=True
	)

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
	description = models.TextField()
	department = models.ForeignKey(
		'recruiters.Department',
		related_name='job_listings',
		on_delete=models.CASCADE
	)
    
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
    
class Suitabilities(models.Model):
    application = models.ForeignKey(
        'applicants.JobApplication',
        related_name = 'application_suitabilities',
        on_delete=models.CASCADE
    )
    magic_score = models.FloatField()
    specific_score = models.FloatField()