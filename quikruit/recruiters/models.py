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

class JobListing(StringBasedModelIDMixin):
	title = models.CharField(max_length=40)
	description = models.TextField()
	department = models.ForeignKey(
		'recruiters.Department',
		related_name='job_listings',
		on_delete=models.CASCADE
	)