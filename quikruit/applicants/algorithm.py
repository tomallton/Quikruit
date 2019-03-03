# These libraries need to be installed first
import tensorflow as tf
import pandas as pd
import numpy as np

from tensorflow.python.data import Dataset

from .models import JobApplication, SkillHobby

# A dictionary which maps programming languages to their position in a one-hot encoding
# For example, a person that knows C and SQL will have the array [0, 1, 0, 0, 0, 0, 0, 1, 0]
programming_languages = {
  "Java": 0,
  "C": 1,
  "C++": 2,
  "Python": 3,
  "HTML": 4,
  "JavaScript": 5,
  "PHP": 6,
  "SQL": 7,
  "Other": 8
}

# is this ok?
a_levels = {
  "Hardware related": 0, # Engineering, Electronics, Computing
  "Software related": 1, # Computing, Information Technology, Software Systems Development, Computer Science
  "Theoretically related": 2, # Mathematics, Physics, Computer Science
  "Other": 3 # Everything else
}

degrees = a_levels

prior_employement = {

}

skills_and_hobbies = {
 # can be excluded?
}

# Encodes all relevant information from applicants using the dictionaries defined earlier
def process_application(application, languages, a_levels, degrees, prior_employment, accepted, index):

    '''
    job_listing = application.job_listing
    applicant = application.applicant
    applicant_skills_and_hobbies = appl.skills_and_hobbies.all()
    applicant_skills = list(applicant_skills_and_hobbies.filter(kind=SkillHobby.SKILL))
    applicant_proglangs = list(applicant_skills_and_hobbies.filter(kind=SkillHobby.PROGRAMMING_LANGUAGE))
    applicant_a_levels = list(applicant.a_levels.all())
    applicant_degrees = list(applicant.degree.all())
    '''

#PLACEHOLDER
def generate_magic_score(application):
  return 0.5

def generate_score(application):
  if len(JobApplication.objects.all()) > 150:
    return supervised_learning(application)
  else:
    return manual_score(application)

def supervised_learning(application):
  # A logistic regression approach

  langs = pd.Series()
  a_lvls - pd.Series()
  degs = pd.Series()
  pr_empl = pd.Series()
  accepted = pd.Series()
  index = 0

  # The model is trained based on candidates that received an answer (rejection, interview or job offer)
  for appl in JobApplication.objects.exclude(status__in = [JobApplication.SENT, JobApplication.ONLINE_TEST_COMPLETED]):
    process_application(appl, langs, a_lvls, degs, pr_empl, accepted, index)
    # index ++

  features = pd.DataFrame({ 'Programming Languages': langs, 'A Levels': a_lvls, 'Degrees': degs, 'Prior Employment': pr_empl, 'Accepted': accepted })
  classifier = train_model(features)
  predictions = classifier.predict()

def train_model(examples):
  pass

# This method will use the job details in order to calculate a score if the supervised learning cannot be used
# Starting from a score of 50, maximum 50 more points can be added or subtracted
# If a required skill/programming language is not present, a fraction of the maximum will be subtracted (but if it is, do not modify the score)
# If an optional skill/language is present, a fraction of the maximum will be added (but if it is not, do not modify the score)
def manual_score(application):
  starting_score = 50
  maximum_to_add = 50
  maximum_to_subtract = -50


