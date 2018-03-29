# Contains all information about the problem - the fitness functions, the
# bounds to the searchspace, etc

def brightness_1(x):
    return x[0]**2

def brightness_2(x):
    return (x[0] - 2)**2

class Problem(object):
    l_bound = [-1000]
    u_bound = [1000]
    no_of_objectives = 2
    brightness_functions = [brightness_1, brightness_2]


prob_inst = Problem()