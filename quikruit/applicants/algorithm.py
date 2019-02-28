import tensorflow as tf

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

prior_employement = {
  
}

def generate_score():
  
  if (there are enough labeled applications on the system):
    return supervised_learning()
  else:
    return manual_score()
    
def supervised_learning():
  # A logistic regression approach
  
# This method will use the job details in order to calculate a score if the supervised learning cannot be used
# Starting from a score of 50, maximum 50 more points can be added or subtracted
# If a required skill/programming language is not present, a fraction of the maximum will be subtracted (but if it is, do not modify the score)
# If an optional skill/language is present, a fraction of the maximum will be added (but if it is not, do not modify the score)
def manual_score():
  starting_score = 50
  maximum_to_add = 50
  maximum_to_subtract = -50
  
  
