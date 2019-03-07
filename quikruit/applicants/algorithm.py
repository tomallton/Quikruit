import math
import pdb

from applicants.models import SkillHobby, Feature, JobApplication

def sigmoid(x):
    return 2 * (1 / (1 + math.pow(math.e, -x / 5)) - 0.5)

def magic_score(application):
    applicant_features = features(application)
    score = 0
    for applicant_feature in applicant_features:
        feature_model = Feature.objects.get(name=applicant_feature, department=application.job_listing.department)
        score += feature_model.weight
    return sigmoid(score);

def application_change(application):
    status = application.status
    change = 0
    if status == JobApplication.INTERVIEW_REQUESTED or status == JobApplication.OFFER_GIVEN:
        change = 0.01
    elif status == JobApplication.REJECTED:
        change = -0.01
    else:
        return

    applicant_features = features(application)

    for applicant_feature in applicant_features:
        change_weight(applicant_feature, change)

def change_weight(feature, change):

    weight = feature.weight + change

    weight = max(weight, 0)
    weight = min(weight, 3)

    feature.weight = weight
    feature.save()

def features(application):
    applicant_features = [];
    applicant = application.applicant
    department = application.job_listing.department

    for a_level in applicant.a_levels.all():
        applicant_features.append(Feature.objects.get(name=a_level.feature_description, department=department))

    for degree in applicant.degree.all():
        applicant_features.append(Feature.objects.get(name=degree.feature_description, department=department))

    for skill in applicant.skills_and_hobbies.filter(kind=SkillHobby.SKILL):
        # pdb.set_trace()
        applicant_features.append(Feature.objects.get(name=skill.feature_description, department=department))

    for programming_language in applicant.skills_and_hobbies.filter(kind=SkillHobby.PROGRAMMING_LANGUAGE):
        applicant_features.append(Feature.objects.get(name=programming_language.feature_description, department=department))

    for prior_employment in applicant.prior_employment.all():
        applicant_features.append(Feature.objects.get(name=prior_employment.feature_description, department=department))

    return applicant_features
