import tensorflow as tf

# A dictionary which maps programming languages to their position in a one-hot encoding
# For example, a person that knows C and Java will have the array [1, 1, 0, 0, 0, 0, 0, 0]
programming_languages = {
  "Java": 0,
  "C": 1,
  "C++": 2,
  "Python": 3,
  "HTML": 4,
  "JavaScript": 5,
  "PHP": 6,
  "Other": 7
}

a_levels = {
  ""
}

def generate_score():
  
  if (there are enough labeled applications on the system):
    return supervised()
  else:
    return manual_score()
    
def supervised():
  # A logistic regression approach
  
# This method will use the job details in order to calculate a score if the supervised learning cannot be used
# Starting from a score of 50, maximum 50 more points can be added or subtracted
# If 
def manual_score():
  starting_score = 50
  maximum_to_add = 50
  maximum_to_subtract = -50
  
  
