from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from applicants.models import JobApplication
from online_tests.models import OnlineTest
from recruiters.models import Suitabilities
from core.models import Notification
from django.urls import reverse
from applicants.algorithm import generate_magic_score

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

@receiver(post_save, sender=JobApplication)
def job_application_save_handler(sender, **kwargs):
  application = kwargs['instance']
  account = application.applicant.account
  job_title = application.job_listing.title

  notification_dict = notification_messages[application.status]
  notification_message = notification_dict['message'].format(job_title)

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

    suitability_score.magic_score = generate_magic_score(application)
    suitability_score.save()