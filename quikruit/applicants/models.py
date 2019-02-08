from django.db import models
from quikruit.mixins import StringBasedModelIDMixin

class ApplicantProfile(StringBasedModelIDMixin):
	account = models.OneToOneField(
		'core.QuikruitAccount', 
		related_name="applicant_profile",
		on_delete=models.CASCADE
	)
    
    name = models.CharField(max_length=40)
    
    #picture =  How/Where do we want to store the pics?
    
    #cv =  How/Where do we want to store the CVs?
    
class PriorEmployment(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name = 'applicant_priorEmployment',
        on_delete = models.CASCADE
    )
    
    company = models.CharField(max_length=60)
    
    position = models.CharField(max_length=60)
    
    length_employment = models.CharField(max_length=30)
    
class ALevel(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name = 'applicant_priorEmployment',
        on_delete = models.CASCADE
    )
    
    subject = models.CharField(max_length=40)
    
    gade = models.CharField(max_length=2)
    
# Create your models here.
