from __future__ import print_function
from helpers import save_logs, save_report, pairwise
import numpy as np
import random
import itertools
import csv
import os

SHAPE = (2,2)
HIGH_POWER = 9999999999
INITIAL_STATES = (1,2)
LENGTHS = (10, 100, 1000)
AB_1 = (0.6, 0.3)
AB_2 = (0.01, 0.3)
AB_3 = (0.01, 0.02)
VARIABLES = (AB_1, AB_2, AB_3)

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

def _report_fractions(states):
    counts1, counts1to2, counts2to1 = 0, 0, 0
    total = float(len(states))
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
    return counts1/total, counts1to2/total, counts2to1/total

def q1ab():
    results = []
    for params in itertools.product(INITIAL_STATES, LENGTHS, VARIABLES):
        initial_state, length, (a,b) = params
        data = [1-a, a, b, 1-b]
        matrix = _construct_matrix(SHAPE, data)
        states = _create_samples(matrix, initial_state, length)
        save_logs(
            filename = "logs/{}_{}_{}_{}.txt".format(initial_state, length, a, b),
            contents = '\n'.join([str(state) for state in states])
        )
        pi1, pi2 = np.linalg.matrix_power(matrix, HIGH_POWER)[0]
        f1, f2, f3 = _report_fractions(states)
        results.append([initial_state, length, a, b, f1, f2, f3, "{}".format(pi1), "{}".format(pi2)])
    save_report(filename = 'results_1ab',
                headers = ['i','T','a','b','frac_state1','frac_1to2','frac_2to1','pi1','pi2'],
                results = results)

def q1c():
    NUM_ITER = 500
    total = float(NUM_ITER)
    results = []
    for params in itertools.product(INITIAL_STATES, LENGTHS, VARIABLES):
        initial_state, length, (a,b) = params
        data = [1-a, a, b, 1-b]
        matrix = _construct_matrix(SHAPE, data)
        counts1, counts1to2, counts2to1 = 0, 0, 0
        for i in range(NUM_ITER):
            states = _create_samples(matrix, initial_state, length)
            prev, last = states[-2], states[-1]
            if last == 1:
                counts1 += 1
                if prev == 2:
                    counts2to1 += 1
            elif last == 2:
                if prev == 1:
                    counts1to2 += 1
        results.append([initial_state, length, a, b, "{:.3f}".format(counts1/total), "{:.3f}".format(counts1to2/total), "{:.3f}".format(counts2to1/total)])
    save_report(filename = 'results_1c',
                headers = ['i','T','a','b','frac_state1','frac_1to2','frac_2to1'],
                results = results)

if __name__=="__main__":
    q1ab()
    q1c()
