import time

t1 = time.time()   # Starting timestamp

import constants as c
from generation import generation
from firefly import firefly, scale_firefly
import matplotlib.pyplot as plt
from problem import  prob_inst as p

p_0 = generation()
p_0.initialize()
x_fitness = []
y_fitness = []

p_0.perform_non_dominated_sort()
no_of_fronts = p_0.count_fronts()

if no_of_fronts == 1:
    q_0 = p_0.random_walk()
else:
    q_0 = p_0.compare_fireflies()

print("First kids == " + (str(len(q_0))))

combinePandQ = generation()
combinePandQ.merge(p_0.population_members)
combinePandQ.merge(q_0)
combinePandQ.perform_non_dominated_sort()
p_next = combinePandQ.population_members[:c.p_size]

p_t = generation()
p_t.merge(p_next)
p_t.perform_non_dominated_sort()
no_of_fronts = p_t.count_fronts()

iter_count = 0
best_fit = []

while(iter_count<c.no_of_iter):
    best_fit.append(p_t.population_members[0].flies)
    print("Iteration counter " + str(iter_count))
    iter_count += 1
    if no_of_fronts == 1:
        q_next = p_t.random_walk()
    else:
        q_next = p_t.compare_fireflies()
    q_next = [firefly(scale_firefly(x.flies)) for x in q_next]

    combinePandQ = generation()
    combinePandQ.merge(p_t.population_members)
    combinePandQ.merge(q_next)
    combinePandQ.perform_non_dominated_sort()
    p_next = combinePandQ.population_members[:c.p_size]
    p_t = generation()
    p_t.merge(p_next)
    p_t.perform_non_dominated_sort()
    no_of_fronts = p_t.count_fronts()
    for member in p_t.population_members:
        x_fitness.append(p.brightness_functions[0](member.flies))
        y_fitness.append(p.brightness_functions[1](member.flies))

print(best_fit)

t2 = time.time()   # Final timestamp
print("Total Time = ", (t2 - t1))

plt.scatter(x_fitness, y_fitness)
plt.show()