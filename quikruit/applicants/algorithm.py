import math

from applicants.models import SkillHobby, Feature, JobApplication

def sigmoid(x):
    return 2 * (1 / (1 + math.pow(math.e, -x / 5)) - 0.5)

def magic_score(applicant):
    applicant_features = features(applicant)
    score = 0
    for applicant_feature in applicant_features:
        feature_model = Feature.objects.get(name=applicant_feature)
        score += feature_model.weight
    return sigmoid(score);

def application_change(applicant, status):
    change = 0
    if status == JobApplication.INTERVIEW_REQUESTED or status == JobApplication.OFFER_GIVEN:
        change = 0.01
    elif status == JobApplication.REJECTED:
        change = -0.01
    else:
        return

    applicant_features = features(applicant)

    for applicant_feature in applicant_features:
        change_weight(applicant_feature, change)

def change_weight(feature, change):
    feature_model = Feature.objects.get(name=feature)

    weight = feature_model.weight + change

    weight = math.max(weight, 0)
    weight = math.min(weight, 3)

    feature_model.weight = weight
    feature_model.save()

def features(application):
    applicant_features = set();
    applicant = application.applicant

    for a_level in applicant.a_levels.all():
        applicant_features.add(str(a_level))

    for degree in applicant.degree.all():
        applicant_features.add(str(degree))

    for skill in applicant.skills_and_hobbies.filter(kind=SkillHobby.SKILL):
        applicant_features.add(str(skill))

    for programming_language in applicant.skills_and_hobbies.filter(kind=SkillHobby.PROGRAMMING_LANGUAGE):
        applicant_features.add(str(programming_language))

    for prior_employment in applicant.prior_employment.all():
        applicant_features.add(str(prior_employment))

    return applicant_features
