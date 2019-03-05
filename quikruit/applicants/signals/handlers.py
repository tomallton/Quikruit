from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from applicants.models import *
from online_tests.models import OnlineTest
from recruiters.models import Suitabilities
from core.models import Notification
from django.urls import reverse
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

perform_selection = False

@receiver(post_save, sender=JobApplication)
def job_application_save_handler(sender, **kwargs):
  application = kwargs['instance']
  account = application.applicant.account
  job_title = application.job_listing.title

  notification_dict = notification_messages[application.status]
  notification_message = notification_dict['message'].format(job_title)

  application_change(application, application.status)

  account.send_notification(notification_message, link=notification_dict['link'])

  try:
    _ = OnlineTest.objects.get(application=application)
  except OnlineTest.DoesNotExist:
    online_test = OnlineTest()
    online_test.application = application
    online_test.save()

    test_notification = Notification()
    test_notification.account = application.applicant.account
    test_notification.message = (
      'An Online Test has been prepared for you for your application to {}. Please click here to complete it.'.format(
        application.job_listing.title
      )
    )
    test_notification.link = reverse('testing_prepare', args=[online_test.model_id])
    test_notification.save()

  try:
    _ = Suitabilities.objects.get(application=application)
  except Suitabilities.DoesNotExist:
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
    all_applications = job_listing.applications.order_by('-application_suitabilites__magic_score')
    applications_count = round(all_applications.count() / 0.25)
    selected_applications = all_applications[:applications_count]
    job_listing.suitable_applications.set(selected_applications)

@receiver(post_save, sender=SkillHobby)
def skill_hobby_save_handler(sender, **kwargs):
  skill_hobby = kwargs['instance']
  
  if skill_hobby.kind == SkillHobby.HOBBY:
    return

  if not Feature.objects.filter(name=skill_hobby.feature_description).exists():
    new_feature = Feature()
    new_feature.name = skill_hobby.feature_description
    new_feature.save()

@receiver(post_save, sender=Degree)
def degree_save_handler(sender, **kwargs):
  degree = kwargs['instance']
  if not Feature.objects.filter(name=degree.feature_description).exists():
    new_feature = Feature()
    new_feature.name = degree.feature_description
    new_feature.save()

@receiver(post_save, sender=ALevel)
def a_level_save_handler(sender, **kwargs):
  a_level = kwargs['instance']
  if not Feature.objects.filter(name=a_level.feature_description).exists():
    new_feature = Feature()
    new_feature.name = a_level.feature_description
    new_feature.save()

@receiver(post_save, sender=PriorEmployment)
def prior_employment_save_handler(sender, **kwargs):
  prior_employment = kwargs['instance']
  if not Feature.objects.filter(name=prior_employment.feature_description).exists():
    new_feature = Feature()
    new_feature.name = prior_employment.feature_description
    new_feature.save()
