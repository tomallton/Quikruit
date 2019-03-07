from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from online_tests.models import OnlineTest, QuestionResponse, TestQuestion
from recruiters.models import RequiredSkill
import random
import pdb

# @receiver(post_save, sender=OnlineTest)
# def online_test_save_handler(sender, **kwargs):
#     test = kwargs['instance']

#     def assign_question(required_skill):
#         suitable_question = random.choice(TestQuestion.objects.filter(tested_skill=required_skill.skill))
#         response = QuestionResponse()
#         response.question = suitable_question
#         response.test = test
#         response.save()

#     if not test.question_responses.exists():
#         for required_skill in test.application.job_listing.required_skills.all():
#             if required_skill.priority == RequiredSkill.COULD:
#                 continue
#             elif required_skill.priority == RequiredSkill.SHOULD:
#                 assign_question(required_skill)
#             else:
#                 for _ in range(3):
#                     assign_question(required_skill)

#         for i in range(5):
#             random_skill = random.choice(test.application.applicant.skills)
#             assign_question()