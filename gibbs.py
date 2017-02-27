from __future__ import print_function
import numpy as np
import random

class Matrix:
    def __init__(self, filepath, shape):
        self.mat = self._load(filepath, shape)

    def _load(self, filepath, shape):
        f = open(filepath).read()
        data = f.split('\n')
        mat = np.array([float(i) for i in data]).reshape(shape)
        return mat

    def shape(self):
        return self.mat.shape

    def get_mean(self, i):
        return np.mean(self.mat[i])

    def value(self, i, j):
        return self.mat[i][j]

def generate_mu_sample(j, tau):
    mean = 0
    for i in range(mat.shape()[1]):
        mean += mat.value(j, i) - (1/tau)
    mean = mean / (500 + (1/(10*tau)))
    var = 1 / (500 + (1/(10*tau)) * tau)
    return np.random.normal(mean, var)

def generate_tau_sample(mat, state):
    alpha = 2502.0
    beta = 0
    for j in range(mat.shape()[0]):
        mu_j = mat.get_mean(j)
        for i in range(mat.shape()[1]):
            beta += (mat.value(j,i) - mu_j) ** 2
    return np.random.gamma(alpha, 1 + 0.5*beta)

if __name__=="__main__":
    NUM_ITER = 1000
    SHAPE = (10,500)
    mat = Matrix('loaddata.txt', SHAPE)
    state = [1.0] # index 0 is the start state for tau
    state += [mat.get_mean(i) for i in range(SHAPE[0])] # all other start states are the mean for respective mu
    for i in range(NUM_ITER):
        ind = random.randint(0,SHAPE[0])
        if ind == 0:
            new_val = generate_tau_sample(mat, state)
        else:
            curr_tau = state[0]
            new_val = generate_mu_sample(ind-1, curr_tau)
        state[ind] = new_val
    print(state)
