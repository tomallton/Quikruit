from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse

from applicants.models import *
from online_tests.models import OnlineTest
from recruiters.models import Suitabilities, JobListing, Department
from core.models import Notification, QuikruitAccount

from applicants.algorithm import magic_score, application_change
import pdb

notification_messages = {
  JobApplication.SENT: {
    'message': 'Your application for {} has been delivered successfully.',
    'link': ''
  },
  JobApplication.ONLINE_TEST_COMPLETED: {
    'message' : '''
    Thank you for completing the online test for your application to {}.
    You should recieve an update on your progress soon.
    ''',
    'link': ''
  },
  JobApplication.INTERVIEW_REQUESTED: {
    'message': '''
    You have been invited to conduct an interview for your application to {}.
    Please contact hr@quikruit.example to arrange one.
    ''',
    'link': 'mailto:hr@quikruit.example'
  },
  JobApplication.INTERVIEW_COMPLETED: {
    'message': '''
    Thank you for completing your interview regarding your application to {}.
    You should recieve an update on your progress soon.
    ''',
    'link': ''
  },
  JobApplication.OFFER_GIVEN: {
    'message': '''
    Congratulations! You have been offered the position of {}.
    please contact hr@quikruit.example to accept the offer.
    ''',
    'link': 'mailto:hr@quikruit.example'
  },
  JobApplication.REJECTED: {
    'message': '''
    Unfortunately, You are no longer being considered for the position of {}.
    We wish you the best of luck in any future endeavours.
    ''',
    'link': ''
  }
}

def send_update_notification(application):
  job_title = application.job_listing.title
  account = application.applicant.account
  notification_dict = notification_messages[application.status]
  notification_message = notification_dict['message'].format(job_title)
  account.send_notification(notification_message, link=notification_dict['link'])

def create_online_test(application):
  if not OnlineTest.objects.filter(application=application).exists():
    online_test = OnlineTest()
    online_test.application = application
    online_test.save()
    online_test.populate()

    application.applicant.account.send_notification(
      'An Online Test has been prepared for you for your application to {}. Please click here to complete it.'.format(
        application.job_listing.title
      ),
      link=reverse('testing_prepare', args=[online_test.model_id])
    )

@receiver(post_save, sender=JobApplication)
def job_application_save_handler(sender, **kwargs):
  application = kwargs['instance']
  account = application.applicant.account
  job_title = application.job_listing.title

  send_update_notification(application)
  application_change(application)
  create_online_test(application)

  if not Suitabilities.objects.filter(application=application).exists():
    suitability_score = Suitabilities()
    suitability_score.application = application
    required_skills = application.job_listing.required_skills.all()
    if not required_skills:
      suitability_score.specific_score = 1
    else:
      applicant_skills = application.applicant.skills_and_hobbies.all()
      shared_skills = len(list(set(required_skills) & set(applicant_skills)))
      suitability_score.specific_score = (shared_skills / len(required_skills))

    suitability_score.magic_score = magic_score(application)
    suitability_score.save()

  if kwargs['created'] and application.job_listing.applications.count() % 15 == 0:
    job_listing = application.job_listing
    all_applications = job_listing.applications.order_by('-application_suitabilities__magic_score')
    applications_count = round(all_applications.count() * 0.25)
    selected_applications = all_applications[:applications_count]
    job_listing.suitable_applications.set(selected_applications)
    for admin_account in QuikruitAccount.objects.filter(is_superuser=True):
      admin_account.send_notification(
        '''
        There are now {} applications to {}. Quikruit has automatically selected {} of them.
        Click here to view the job listing.
        '''.format(job_listing.applications.count(), job_listing.title, job_listing.suitable_applications.count()),
        link=reverse('admin:recruiters_joblisting_change', args=[job_listing.model_id])
      )

def add_feature(description):
  if not Feature.objects.filter(name=description).exists():
    for d in Department.objects.all():
      new_feature = Feature()
      new_feature.department = d
      new_feature.name = description
      new_feature.save()

@receiver(post_save, sender=SkillHobby)
def skill_hobby_save_handler(sender, **kwargs):
  skill_hobby = kwargs['instance']
  
  if kwargs['created'] and skill_hobby.kind == SkillHobby.UNCATEGORISED:
    for admin_account in QuikruitAccount.objects.filter(is_superuser=True):
      admin_account.send_notification(
        '''
        An applicant has added a new Skill / Hobby to the database ({}), please click here to
        correctly categorise it.
        '''.format(skill_hobby.name),
        link=reverse('admin:applicants_skillhobby_change', args=[skill_hobby.name])
      )

  if skill_hobby.kind != SkillHobby.HOBBY:
    add_feature(skill_hobby.feature_description)

@receiver(post_save, sender=Degree)
def degree_save_handler(sender, **kwargs):
  add_feature(kwargs['instance'].feature_description)

@receiver(post_save, sender=ALevel)
def a_level_save_handler(sender, **kwargs):
  add_feature(kwargs['instance'].feature_description)

@receiver(post_save, sender=PriorEmployment)
def prior_employment_save_handler(sender, **kwargs):
  add_feature(kwargs['instance'].feature_description)
