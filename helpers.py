import numpy as np
import csv
import itertools

RESULTS = 'results/{}'

def save_logs(filename, contents):
    with open(RESULTS.format(filename), 'w') as f:
        f.write(contents)

def save_report(filename, headers, results):
    filepath = RESULTS.format(filename + '.csv')
    with open(filepath, 'w') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for result in results:
            w.writerow(result)

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

def load_given_data():
    with open('loaddata.txt', 'r') as f:
        data = f.read()
    data = [float(i) for i in data.split('\n')]
    data = np.array(data).reshape(10,500)
    return data
