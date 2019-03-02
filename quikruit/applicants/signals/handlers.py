from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from applicants.models import JobApplication
from online_tests.models import OnlineTest
from recruiters.models import Suitabilities
from core.models import Notification
import pdb
from django.urls import reverse
from applicants.algorithm import generate_magic_score

@receiver(post_save, sender=JobApplication)
def job_application_save_handler(sender, **kwargs):
  sent_application_notification = Notification()
  sent_application_notification.message = (
    "Your application for {} has been delivered successfully.".format(kwargs['instance'].job_listing.title)
  )
  sent_application_notification.account = kwargs['instance'].applicant.account
  sent_application_notification.save()

  try:
    _ = OnlineTest.objects.get(application=kwargs['instance'])
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

  try:
    _ = Suitabilities.objects.get(application=kwargs['instance'])
  except Suitabilities.DoesNotExist:
    suitability_score = Suitabilities()
    suitability_score.application = kwargs['instance']
    required_skills = kwargs['instance'].job_listing.required_skills.all()
    if not required_skills:
      suitability_score.specific_score = 1
    else:
      applicant_skills = kwargs['instance'].applicant.skills_and_hobbies.all()
      shared_skills = len(list(set(required_skills) & set(applicant_skills)))
      suitability_score.specific_score = (shared_skills / len(required_skills))
    
    suitability_score.magic_score = generate_magic_score(kwargs['instance'])
    suitability_score.save()