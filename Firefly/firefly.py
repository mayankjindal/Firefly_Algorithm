import constants as c
from problem import prob_inst as p
from random import random
import pprint

class firefly(object):
    def __init__(self, keeda=None):
        if keeda is None:
            self.flies = [random() * (2 ** (c.len_of_bit_str)) for x in range(0, c.no_of_var)]
            self.flies = scale_firefly(self.flies)
        else:
            self.flies = keeda
        self.front = None
        self.brightness_values = []
        self.np = 0
        self.Sp = set()
        self.avg_brightness = 0
        self.evaluate_brightness()

    def print_firefly(self):
        pprint.pprint('Firefly: ' + repr(self.flies) \
                      + '\nbrightness ' + repr(self.brightness_values) \
                      + '\nnp: ' + repr(self.np) \
                      + '\nFront: ' + repr(self.front) \
                      + '\navg_brightness: ' + repr(self.avg_brightness))

    def evaluate_brightness(self):
        self.brightness_values = [y(self.flies) for y in p.brightness_functions]

    def dominates_lesser(self, firefly2):
        lesserorequal = 0
        for x, y, in zip(self.brightness_values, firefly2.brightness_values):
            if x<=y:
                lesserorequal += 1
        if(lesserorequal == p.no_of_objectives):
            return True
        else:
            return False

    def dominates_greater(self, firefly2):
        greaterorequal = 0
        for x, y in zip(self.brightness_values, firefly2.brightness_values):
            if x >= y:
                greaterorequal += 1
        if (greaterorequal == p.no_of_objectives):
            return True
        else:
            return False

def scale_firefly(crud):
    temp = [(z + (y -z) * x / ((2 ** c.len_of_bit_str) - 1)) for x, y, z in
            zip(crud, p.u_bound, p.l_bound)]
    return temp