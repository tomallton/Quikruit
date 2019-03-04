
import math

    def magicScore(applicant):


    # Applies a sigmoid function to a given value.
    #
    # Returns a value between 0 and 1 not inclusive proportional to the input x.
    #
    def sigmoid(x):
        return 2 * (1 / (1 + math.pow(math.e, -x / 5)) - 0.5)
