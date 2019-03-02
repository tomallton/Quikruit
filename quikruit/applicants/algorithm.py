# These libraries need to be installed first
import tensorflow as tf
import pandas as pd
import numpy as np

from tensorflow.python.data import Dataset

from .models import JobApplication

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

degree = a_levels

prior_employement = {
  
}

skills_and_hobbies = {
 # can be excluded? 
}

def generate_magic_score(application):
  return 0.5 #PLACEHOLDER

def generate_score(application):
  if (len(JobApplication.objects.all()) > 150):
    return supervised_learning(application)
  else:
    return manual_score(application)
    
def supervised_learning(application):
  # A logistic regression approach
  
  # Positive applicants (i.e. ones who were offered a job)
  for application in (JobApplication.objects.filter(status=JobApplication.OFFER_GIVEN)): #?
    job_listing = application.job_listing
    applicant = application.applicant
    applicant_skills_and_hobbies = list(applicant.skills_and_hobbies.all())
    applicant_a_levels = list(applicant.a_levels.all())
    applicant_degrees = list(applicant.degree.all())

  
# This method will use the job details in order to calculate a score if the supervised learning cannot be used
# Starting from a score of 50, maximum 50 more points can be added or subtracted
# If a required skill/programming language is not present, a fraction of the maximum will be subtracted (but if it is, do not modify the score)
# If an optional skill/language is present, a fraction of the maximum will be added (but if it is not, do not modify the score)
def manual_score(application):
  starting_score = 50
  maximum_to_add = 50
  maximum_to_subtract = -50
  
  
