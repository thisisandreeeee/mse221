import csv
import itertools

def save_logs(filename, contents):
    with open(RESULTS.format(filename), 'w') as f:
        f.write(contents)

def save_report(params, results):
    filepath = RESULTS.format('results.csv')
    initial_state, length, (a,b) = params
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            w = csv.writer(f)
            w.writerow(['i','T','a','b','frac_state1','frac_1to2','frac_2to1','pi1','pi2'])
    r1, r2, r3, pi1, pi2 = results
    with open(filepath, 'a') as f:
        w = csv.writer(f)
        w.writerow([initial_state, length, a, b, r1, r2, r3, pi1, pi2])

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)
