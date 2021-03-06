from django.db import models
from quikruit.mixins import StringBasedModelIDMixin
from django.utils import timezone
from quikruit.settings import MEDIA_ROOT

s = lambda s: s.strip(' \t\n\r')

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
        blank=True,
        null=True
    )

    cv = models.FileField(
        upload_to=cv_directory_path,
        blank=True,
        null=True)

    skills_and_hobbies = models.ManyToManyField(
        'applicants.SkillHobby',
        through='applicants.SkillHobbyLevel',
        related_name='suitable_applicants'
    )

    def __repr__(self):
        return "<Applicant: {0} [ID: {1}]>".format(self.name, self.model_id)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.account.email)

    @property
    def skills(self):
        return self.skills_and_hobbies.filter(kind=SkillHobby.SKILL)

    @property
    def programming_languages(self):
        return self.skills_and_hobbies.filter(kind=SkillHobby.PROGRAMMING_LANGUAGE)

    @property
    def hobbies(self):
        return self.skills_and_hobbies.filter(kind=SkillHobby.HOBBY)


class PriorEmployment(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name = 'prior_employment',
        on_delete = models.CASCADE
    )
    company = models.CharField(max_length=60)
    position = models.CharField(max_length=60)

    @property
    def feature_description(self):
        return '{} [Prior Employment]'.format(s(self.company))

    def __str__(self):
        return '{}|{} [Prior Employment]'.format(s(self.company), s(self.position))

class Degree(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name = 'degree',
        on_delete = models.CASCADE
    )
    institution = models.CharField(max_length=60)
    qualification = models.CharField(max_length=60)

    # Since Degrees gave have different ways of being awarded in
    # Different countries, the `level` attribute will not have
    # the expected 1st, 2:1, 2:2 etc. choices.
    level_awarded = models.CharField(max_length=20)

    @property
    def feature_description(self):
        return '{}|{} [Degree]'.format(s(self.qualification), s(self.level_awarded))

    def __str__(self):
        return "{}|{}|{} [Degree]".format(s(self.institution), s(self.qualification), s(self.level_awarded))

class ALevel(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name = 'a_levels',
        on_delete = models.CASCADE
    )
    subject = models.CharField(max_length=40)
    grade = models.CharField(max_length=2)

    @property
    def feature_description(self):
        return str(self)

    def __str__(self):
        return "{}|Grade {} [A-Level]".format(s(self.subject), s(self.grade))

class SkillHobbyLevel(models.Model):
    applicant = models.ForeignKey(
        'applicants.ApplicantProfile',
        related_name="skill_hobby_levels",
        on_delete=models.CASCADE
    )

    skillhobby = models.ForeignKey(
        'applicants.SkillHobby',
        related_name="applicant_levels",
        on_delete=models.CASCADE
    )

    level_choices = ((i,"{}".format(i)) for i in range(0,11))
    level = models.IntegerField(choices=level_choices)

    def __str__(self):
        return "{}|{}|{}".format(self.applicant.name, self.skillhobby, self.level)

class SkillHobby(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True,
        primary_key=True
    )
    SKILL                = 0
    HOBBY                = 1
    PROGRAMMING_LANGUAGE = 2
    UNCATEGORISED        = 3
    kind_choices = (
        (SKILL, "Skill"),
        (HOBBY, "Hobby"),
        (PROGRAMMING_LANGUAGE, "Programming Language"),
        (UNCATEGORISED, 'Currently Uncategorised')
    )
    kind = models.IntegerField(choices=kind_choices)

    @property
    def feature_description(self):
        return str(self)

    def __str__(self):
        return "{1} [{0}]".format(self.get_kind_display(), self.name)

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
    date_submitted = models.DateTimeField(auto_now_add=True)

    SENT                   = 0
    REJECTED               = 1
    ONLINE_TEST_COMPLETED  = 2
    INTERVIEW_REQUESTED    = 3
    INTERVIEW_COMPLETED    = 4
    OFFER_GIVEN            = 5

    status_choices = (
        (SENT, 'Application sent'),
        (ONLINE_TEST_COMPLETED, 'Online test completed'),
        (INTERVIEW_REQUESTED, 'Interview requested'),
        (INTERVIEW_COMPLETED, 'Interview completed'),
        (REJECTED, 'No longer being considered'),
        (OFFER_GIVEN, 'Job offer sent'),
    )
    status = models.IntegerField(choices=status_choices, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} -> {}'.format(self.applicant.name, self.job_listing.title)

class Feature(models.Model):
    name = models.CharField(max_length=50)
    weight = models.FloatField(default=1.0)
    department = models.ForeignKey(
        'recruiters.Department',
        related_name='relevant_features',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
