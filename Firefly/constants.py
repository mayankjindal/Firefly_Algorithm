#stores MOFA constants
from problem import prob_inst as p

len_of_bit_str = 32
p_size = 500
beta = 1
alpha = 0.01*(p.u_bound[0]-p.l_bound[0])
gamma = 0.5/((p.u_bound[0]-p.l_bound[0])**2)
no_of_iter = 50
no_of_var = 1