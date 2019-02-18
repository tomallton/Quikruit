from django.db import models
from quikruit.mixins import StringBasedModelIDMixin
from django.utils import timezone

def _directory_path(instance, filename, model):
    split_file_name = filename.split(sep='.')
    filetype = split_file_name[len(split_file_name) - 1]
    now = timezone.now()
    # File will be uploaded to 
    # MEDIA_ROOT/applicant_profiles/pictures/user_<id>/<filename>
    return 'employee_profile/{t}/user_{uid}/{y}_{m}_{d}.{f}'.format(
        t=model,
        uid=instance.account.model_id, 
        y=now.year, 
        m=now.month, 
        d=now.day,
        f=filetype
    )

def cv_directory_path(instance, filename):
    return _directory_path(instance, filename, 'CVs')

def profile_picture_directory_path(instance, filename):
    return _directory_path(instance, filename, 'ProfilePictures')

class ApplicantProfile(StringBasedModelIDMixin):
    account = models.OneToOneField(
		'core.QuikruitAccount', 
		related_name="applicant_profile",
		on_delete=models.CASCADE
	)
    
    name = models.CharField(max_length=40)
    
    picture = models.ImageField(
        upload_to=profile_picture_directory_path,
        blank=True
    )

    cv = models.FileField(
        upload_to=cv_directory_path,
        blank=True)

    jobs = models.ManyToManyField(
        'recruiters.JobListing',
        through='applicants.JobApplication',
        related_name='applicants'
    )
    
class PriorEmployment(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name = 'prior_employment',
        on_delete = models.CASCADE
    )
    company = models.CharField(max_length=60)
    position = models.CharField(max_length=60)
    employed_from  = models.DateField()
    employed_until = models.DateField()

    @property
    def length_of_employment(self):
        return self.employed_until - self.employed_from
     
    
class Degree(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name = 'degree',
        on_delete = models.CASCADE
    )
    institution = models.CharField(max_length=60)
    qualification = models.CharField(max_length=60)
    date_awarded = models.DateField()

    # Since Degrees gave have different ways of being awarded in
    # Different countries, the `level` attribute will not have
    # the expected 1st, 2:1, 2:2 etc. choices. 
    level_awarded = models.CharField(max_length=20)

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
    SKILL                = 0
    HOBBY                = 1
    PROGRAMMING_LANGUAGE = 2
    kind_choices = (
        (SKILL, "Skill"),
        (HOBBY, "Hobby"),
        (PROGRAMMING_LANGUAGE, "Programming Language")
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


