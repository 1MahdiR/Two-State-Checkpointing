
import subprocess
import os
import sys
from time import time
from random import randint
import matplotlib.pyplot as plt

from Task import Task, Fault
from Core import Core, Volatage_Frequency

from bcolor import *

NULL = open(os.devnull, 'w')
STDOUT = sys.stdout

PLOT_ALL = True
schemes_labels = ["TsCp", "TsCp-DVS", "Non-Uniform", "Uniform", "R_target(0.99999)"]

vf_1 = Volatage_Frequency(0.72, 0.59)
vf_2 = Volatage_Frequency(1.23, 0.97)

i_sub = 0.1
c_eff = 1
delta = 3

lambda_0 = 10 ** -4

c = Core([vf_1, vf_2], lambda_0, i_sub, c_eff, delta)

checkpoint_overhead = 10
rollback_overhead = 10

u = 0.57
script_names = [
    "mibench/automotive/basicmath/rad2deg.py",
    "mibench/telecomm/FFT/runme_large.py",
    "mibench/telecomm/CRC32/crc_32.py",
    "mibench/network/dijkstra/runme_large.py",
    "mibench/network/dijkstra/runme_small.py",
    "mibench/automotive/qsort/qsort_large.py",
    "mibench/automotive/bitcount/bitcnt_1.py",
    "mibench/automotive/bitcount/bitcnt_4.py",
    "mibench/automotive/bitcount/bitcnt_3.py",
    "mibench/automotive/bitcount/bitcnt_2.py",
    "mibench/automotive/basicmath/basicmath_small.py",
    "mibench/automotive/basicmath/isqrt.py",
    "mibench/automotive/basicmath/rad2deg.py",
    "mibench/automotive/basicmath/cubic.py",
    "mibench/automotive/basicmath/basicmath_large.py",
]

for script in script_names:
    t1 = time()
    subprocess.call(["python3", script], stdout=NULL)
    t2 = time()

    et = t2 - t1
    d = et / u

    if et >= 1000:
        et = int(str(et)[:3])
        d = int(str(d)[:3])
    elif et < 200:
        while et < 200:
            et = et * 10
            d = d * 10
        et = round(et)
        d = round(d)

    f1 = randint(50, et)
    f2 = randint(100, et + 100)

    f_ls = [Fault(f1), Fault(f2)]
    print(f_ls, et, d)

    task = Task(et, len(f_ls), d, c, f_ls, checkpoint_overhead, rollback_overhead)

    data = []

    try:
        print(BOLD + ("### Starting '%s' ###" % script) + ENDC)
        print(task)
        print(BOLD + "--- TsCp Begin ---" + ENDC)
        data.append(task.run())
        print(BOLD + "--- TsCp End ---" + ENDC)

        print()

        print(BOLD + "--- TsCp-DVS Begin ---" + ENDC)
        data.append(task.run_dvs())
        print(BOLD + "--- TsCp-DVS End ---" + ENDC)

        print()

        print(BOLD + "--- Non-Uniform Begin ---" + ENDC)
        data.append(task.run_non_uniform())
        print(BOLD + "--- Non-Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Uniform Begin ---" + ENDC)
        data.append(task.run_uniform())
        print(BOLD + "--- Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Reliability-Target Begin ---" + ENDC)
        data.append(task.run_reliability_taret(0.99999))
        print(BOLD + "--- Reliability-Target End ---" + ENDC)
        print(BOLD + ("### '%s' Finished ###" % script) + ENDC)
    except Exception:
        print(FAIL + "Task failed!!!" + ENDC)
        continue

    et_ls = []
    e_ls = []
    r_ls = []
    k_ls = []
    deadline = d
    
    for i in data:
        et, e, r, k = i
        et_ls.append(et)
        e_ls.append(e)
        r_ls.append(r)
        k_ls.append(k)

    if PLOT_ALL:
            plt.figure() 
            ax = plt.subplot(1, 1, 1)
            bar_width = 0.35
            ax.bar(schemes_labels, et_ls, bar_width, label="et_ls", color="green")
            ax.set_ylim(min(et_ls) - 100, max(et_ls) + 100)
            for i, v in enumerate(et_ls):
                ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
            ax.axhline(y=deadline, color='red', linestyle='-', label=f'Deadline ({d})')  
            plt.title("Execution Time by Different Schemes")
            plt.ylabel("execution time")
            plt.tight_layout()
            plt.title(script)
            plt.show()

            plt.figure() 
            ax = plt.subplot(1, 1, 1)
            bar_width = 0.35
            ax.bar(schemes_labels, e_ls, bar_width, label="e_ls", color="orange")
            ax.set_ylim(min(e_ls) - 1000, max(e_ls) + 1000)
            for i, v in enumerate(e_ls):
                ax.text(i, v + 0.5, str(round(v, 2)), ha='center', va='bottom')  
            plt.title("Energy Consumption by Different Schemes")
            plt.ylabel("energy consumption")
            plt.tight_layout()
            plt.title(script)
            plt.show()

            plt.figure() 
            ax = plt.subplot(1, 1, 1)
            bar_width = 0.35
            ax.bar(schemes_labels, r_ls, bar_width, label="r_ls", color="blue")
            ax.set_ylim(min(r_ls) - 0.01, 1.001)
            for i, v in enumerate(r_ls):
                ax.text(i, v, str(round(v, 6)), ha='center', va='bottom')  
            plt.title("Reliability by Different Schemes")
            plt.ylabel("reliability")
            plt.tight_layout()
            plt.title(script)
            plt.show()

            plt.figure() 
            ax = plt.subplot(1, 1, 1)
            bar_width = 0.35
            ax.bar(schemes_labels, k_ls, bar_width, label="k_ls", color="green")
            ax.set_ylim(min(k_ls) - 1, max(k_ls) + 1)
            for i, v in enumerate(k_ls):
                ax.text(i, v, str(round(v, 2)), ha='center', va='bottom')  
            plt.title("Number of Checkpoints by Different Schemes")
            plt.ylabel("number of checkpoints")
            plt.tight_layout()
            plt.title(script)
            plt.show()

NULL.close()



