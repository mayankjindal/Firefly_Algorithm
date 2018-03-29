import constants as c
import numpy as np
from firefly import firefly
from collections import defaultdict
from problem import prob_inst as p

class generation(object):
    def __init__(self):
        self.population_members = []
        self.no_of_fronts = 0

    def initialize(self):
        self.population_members  = [firefly() for i in range(0, c.p_size)]

    def merge(self, Qt):
        self.population_members += Qt
        self.count_fronts()

    def print_population(self):
        print('----Population begin----')
        [x.print_firefly() for x in self.population_members]
        print('----Population End----')

    def perform_non_dominated_sort(self):
        for x in self.population_members:
            x.np = 0
        front_counter = 1
        temp_front = []
        next_front = []

        for a in self.population_members:
            for b in self.population_members:
                if (a != b):
                    if (a.dominates_lesser(b)):
                        a.Sp.add(b)
                    elif (b.dominates_lesser(a)):
                        a.np += 1
        groups = defaultdict(list)
        for obj in self.population_members:
            groups[obj.np].append(obj)
        new_list = list(groups.values())
        temp_front = new_list[0]
        for x in temp_front:
            x.front = front_counter
        front_counter += 1
        while len(temp_front) > 0:
            list_of_Sp = []
            list_of_np_zero = []
            for x in temp_front:
                for y in x.Sp:
                    list_of_Sp.append(y)
            for x in list_of_Sp:
                x.np -= 1
                if x.np == 0:
                    x.front = front_counter
                    list_of_np_zero.append(x)
            front_counter += 1
            temp_front = list_of_np_zero
        self.population_members.sort(key=lambda  x: x.front)
        self.no_of_fronts = front_counter

    def move_firefly(self, x, y):
        r = 0
        for i in range(0, c.no_of_var):
            r += (y.flies[i] - x.flies[i])**2
        r = abs(r**0.5)
        new_location = [(y.flies[i] + c.beta*(np.exp(-(c.gamma)*r))*(x.flies[i] - y.flies[i]) + c.alpha*np.random.normal(0.5, 0.2, 1)[0]) for i in range(0, c.no_of_var)]
        return new_location

    def compare_fireflies(self):
        child = []
        new_fireflies = []
        first_front = []
        for x in self.population_members:
            if x.front == 1:
                first_front.append(x)
        random_weights = np.random.dirichlet(np.ones(p.no_of_objectives), size=1)
        for x in self.population_members:
            x.avg_brightness = [(random_weights[0][i] * x.brightness_values[i]) for i in range(0, p.no_of_objectives)][0]
        for x in self.population_members:
            brightest_firefly = first_front[0]
            brightest_value = 0
            for y in first_front:
                r = 0
                for i in range(0, c.no_of_var):
                    r += (y.flies[i] - x.flies[i])**2
                b = c.beta*(np.exp(-(c.gamma)*r))
                if b > brightest_value:
                    brightest_value = b
                    brightest_firefly = y
            child = self.move_firefly(x, brightest_firefly)
            new_fireflies += [firefly(child)]

        return new_fireflies

    def random_walk(self):
        # Initialising random weights
        new_fireflies = []
        random_weights = np.random.dirichlet(np.ones(p.no_of_objectives), size=1)
        self.population_members[0].avg_brightness = [(random_weights[i] * self.population_members[0].brightness_values[i]) for i in range(0, p.no_of_objectives)]
        gbest = self.population_members[0].avg_brightness
        # Calculating average brightness and global best
        for x in self.population_members:
            x.avg_brightness = [(random_weights[0][i] * x.brightness_values[i]) for i in range(0, p.no_of_objectives)][0]
            gbest = min(gbest, x.avg_brightness)
        for x in self.population_members:
            new_location = [(gbest + c.alpha*np.random.normal(0.5, 0.2, 1)[0]) for i in range(0, c.no_of_var)]
            new_fireflies += firefly(new_location)
        return new_fireflies

    def count_fronts(self):
        frontset = set()
        for x in self.population_members:
            frontset.add(x.front)
        self.no_of_fronts = len(frontset)
        return self.no_of_fronts