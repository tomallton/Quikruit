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
        related_name = 'prior_employment',
        on_delete = models.CASCADE
    )
    company = models.CharField(max_length=60)
    position = models.CharField(max_length=60)
    length_employment = models.CharField(max_length=30)
    
class ALevel(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name = 'a_levels',
        on_delete = models.CASCADE
    )
    subject = models.CharField(max_length=40)
    grade = models.CharField(max_length=2)

class SkillHobbyLevel(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name="skills_and_hobbies",
        on_delete=models.CASCADE
    )

    skillhobby = models.ForeignKey(
        'applicants.SkillHobby',
        related_name="skill_hobby_levels",
        on_delete=models.CASCADE
    )

    level_choices = ((i,"{}".format(i)) for i in range(1,6))
    level = models.IntegerField(choices=level_choices)

class SkillHobby(StringBasedModelIDMixin):
    name = models.CharField(
        max_length=40,
        unique=True
    )
    SKILL = 0
    HOBBY = 1
    kind_choices = (
        (SKILL, "Skill"),
        (HOBBY, "Hobby")
    )
    kind = models.IntegerField(choices=kind_choices)

class JobApplication(StringBasedModelIDMixin):
    job_listing = models.ForeignKey(
        'recruiters.JobListing',
        related_name='applications',
        on_delete=models.CASCADE
    )
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name='job_applications',
        on_delete=models.CASCADE
    )
    cover_letter = models.TextField(blank=True)
    date_submitted = models.DateTimeField(null=True)

    IN_PROGRESS            = 0
    SENT                   = 1
    UNDER_CONSIDERATION    = 2
    ONLINE_TEST_REQUESTED  = 3
    ONLINE_TEST_COMPLETED  = 4
    REJECTED               = 5
    OFFER_GIVEN            = 6
    EMPLOYED               = 7

    status_choices = (
        (IN_PROGRESS, "In progress"),
        (SENT, "Application sent"),
        (UNDER_CONSIDERATION, "Application under consideration"),
        (ONLINE_TEST_REQUESTED, "Online test requested"),
        (REJECTED, "No longer being considered"),
        (OFFER_GIVEN, "Job offer sent"),
        (EMPLOYED, "Offer accepted")
    )


