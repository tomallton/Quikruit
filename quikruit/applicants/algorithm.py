
import math
from applicants.models import SkillHobby, Feature

    def magicScore(applicant):

        applicantFeatures = set();

        for (aLevel in applicant.a_levels.all()):
            applicantFeatures.add(str(aLevel))

        for (degree in applicant.degree.all()):
            applicantFeatures.add(str(degree))

        for (skill in applicant.skills_and_hobbies.filter(kind=SkillHobby.SKILL):
            applicantFeatures.add(str(skill))

        for (programming_language in applicant.skills_and_hobbies.filter(kind=SkillHobby.PROGRAMMING_LANGUAGE):
            applicantFeatures.add(str(programming_language))

        for (prior_employment in applicant.prior_employment.all()):
            applicantFeatures.add(str(prior_employment))

        score = 0

        for (applicantFeature in applicantFeatures):
            feature_model = Feature.objects.get(name=applicantFeature)
            score += feature_model.weight

        return sigmoid(score);

    # Applies a sigmoid function to a given value.
    #
    # Returns a value between 0 and 1 not inclusive proportional to the input x.
    #
    def sigmoid(x):
        return 2 * (1 / (1 + math.pow(math.e, -x / 5)) - 0.5)
