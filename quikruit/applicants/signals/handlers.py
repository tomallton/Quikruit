from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from applicants.models import JobApplication
from online_tests.models import OnlineTest
from core.models import Notification
import pdb
from django.urls import reverse

@receiver(post_save, sender=JobApplication)
def job_application_save_handler(sender, **kwargs):
  sent_application_notification = Notification()
  sent_application_notification.message = (
    "Your application for {} has been delivered successfully.".format(kwargs['instance'].job_listing.title)
  )
  sent_application_notification.account = kwargs['instance'].applicant.account
  sent_application_notification.save()

  try:
    online_test = OnlineTest.objects.get(application=kwargs['instance'])
  except OnlineTest.DoesNotExist:
    online_test = OnlineTest()
    online_test.application = kwargs['instance']
    online_test.save()

    test_notification = Notification()
    test_notification.account = kwargs['instance'].applicant.account
    test_notification.message = (
      'An Online Test has been prepared for you for your application to {}. Please click here to complete it.'.format(
        kwargs['instance'].job_listing.title
      )
    )
    test_notification.link = reverse('testing_prepare', args=[online_test.model_id])
    test_notification.save()  