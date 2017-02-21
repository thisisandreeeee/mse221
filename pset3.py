from __future__ import print_function
from helpers import save_logs, save_report, pairwise
import numpy as np
import random
import itertools
import csv
import os

RESULTS = 'results/{}'
SHAPE = (2,2)
HIGH_POWER = 9999999999

def _construct_matrix(shape, data):
    mat = np.array([float(val) for val in data]).reshape(shape)
    assert all([row.sum() == 1 for row in mat])
    return mat

def _create_samples(matrix, initial_state, length):
    curr_state = initial_state
    states = []
    for i in range(length):
        states.append(curr_state)
        probs = matrix[curr_state - 1]
        rnd = random.uniform(0,1)
        curr_state = 1 if rnd < probs[0] else 2
    return states

def _report_fractions(params, states, invariant_distribution):
    counts1, counts1to2, counts2to1 = 0, 0, 0
    total = float(len(states))
    pi1, pi2 = invariant_distribution
    for _curr, _next in pairwise(states):
        if _curr == 1:
            counts1 += 1
            if _next == 2:
                counts1to2 += 1
        elif _curr == 2:
            if _next == 1:
                counts2to1 += 1
    # handling index -1
    if _next == 1:
        counts1 += 1
    save_report(params,
                results = (counts1/total, counts1to2/total, counts2to1/total, pi1, pi2))

def question_1():
    initial_states = (1,2)
    lengths = (10, 100, 1000)
    AB_1 = (0.6, 0.3)
    AB_2 = (0.01, 0.3)
    AB_3 = (0.01, 0.02)
    variables = (AB_1, AB_2, AB_3)
    for params in itertools.product(initial_states, lengths, variables):
        initial_state, length, (a,b) = params
        data = [1-a, a, b, 1-b]
        matrix = _construct_matrix(SHAPE, data)
        states = _create_samples(matrix, initial_state, length)
        save_logs(
            filename = "logs/{}_{}_{}_{}.txt".format(initial_state, length, a, b),
            contents = '\n'.join([str(state) for state in states])
        )
        invariant_distribution = np.linalg.matrix_power(matrix, HIGH_POWER)[0]
        _report_fractions(params, states, invariant_distribution)

if __name__=="__main__":
    question_1()
