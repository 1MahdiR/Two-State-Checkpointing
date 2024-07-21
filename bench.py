from Core import Core, Volatage_Frequency
from Task import Task, Fault
from bcolor import *

class bench_1:
    vf_1 = Volatage_Frequency(2, 1.5)
    vf_2 = Volatage_Frequency(3, 2)

    i_sub = 1
    c_eff = 1
    delta = 3

    lambda_0 = 10 ** -4

    c = Core([vf_1, vf_2], lambda_0, i_sub, c_eff, delta)

    f1 = Fault(170)
    f2 = Fault(490)

    fault_ls = [f1, f2]

    checkpoint_insertion_overhead = 10
    rollback_overhead = 10
    et = 420
    d = 740


    t = Task(et, len(fault_ls), d, c, fault_ls, 
             checkpoint_insertion_overhead, rollback_overhead)

    def run_bench():

        data = []

        print(BOLD + ("### Starting '%s' ###" % bench_1.__name__) + ENDC)
        print(BOLD + "--- TsCp Begin ---" + ENDC)
        data.append(bench_1.t.run())
        print(BOLD + "--- TsCp End ---" + ENDC)

        print()

        print(BOLD + "--- TsCp-DVS Begin ---" + ENDC)
        data.append(bench_1.t.run_dvs())
        print(BOLD + "--- TsCp-DVS End ---" + ENDC)

        print()

        print(BOLD + "--- Non-Uniform Begin ---" + ENDC)
        data.append(bench_1.t.run_non_uniform())
        print(BOLD + "--- Non-Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Uniform Begin ---" + ENDC)
        data.append(bench_1.t.run_uniform())
        print(BOLD + "--- Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Reliability-Target Begin ---" + ENDC)
        data.append(bench_1.t.run_reliability_taret(0.99999))
        print(BOLD + "--- Reliability-Target End ---" + ENDC)
        print(BOLD + ("### '%s' Finished ###" % bench_1.__name__) + ENDC)

        print()
        return data
    
class bench_2:
    vf_1 = Volatage_Frequency(0.75, 0.75)
    vf_2 = Volatage_Frequency(1, 1)
    vf_3 = Volatage_Frequency(1.25, 1.25)
    vf_4 = Volatage_Frequency(1.5, 1.5)

    i_sub = 1
    c_eff = 1
    delta = 3

    lambda_0 = 10 ** -4

    c = Core([vf_1, vf_2, vf_3, vf_4], lambda_0, i_sub, c_eff, delta)

    f1 = Fault(220)
    f2 = Fault(330)

    fault_ls = [f1, f2]

    checkpoint_insertion_overhead = 10
    rollback_overhead = 10

    et = 550
    d = 1080


    t = Task(et, len(fault_ls), d, c, fault_ls, 
             checkpoint_insertion_overhead, rollback_overhead)

    def run_bench():

        data = []

        print(BOLD + ("### Starting '%s' ###" % bench_2.__name__) + ENDC)
        print(BOLD + "--- TsCp Begin ---" + ENDC)
        data.append(bench_2.t.run())
        print(BOLD + "--- TsCp End ---" + ENDC)

        print()

        print(BOLD + "--- TsCp-DVS Begin ---" + ENDC)
        data.append(bench_2.t.run_dvs())
        print(BOLD + "--- TsCp-DVS End ---" + ENDC)

        print()

        print(BOLD + "--- Non-Uniform Begin ---" + ENDC)
        data.append(bench_2.t.run_non_uniform())
        print(BOLD + "--- Non-Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Uniform Begin ---" + ENDC)
        data.append(bench_2.t.run_uniform())
        print(BOLD + "--- Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Reliability-Target Begin ---" + ENDC)
        data.append(bench_2.t.run_reliability_taret(0.99999))
        print(BOLD + "--- Reliability-Target End ---" + ENDC)
        print(BOLD + ("### '%s' Finished ###" % bench_2.__name__) + ENDC)

        print()
        return data
    
class bench_3:
    vf_1 = Volatage_Frequency(0.75, 0.75)
    vf_2 = Volatage_Frequency(1, 1)
    vf_3 = Volatage_Frequency(1.25, 1.25)
    vf_4 = Volatage_Frequency(1.5, 1.5)

    i_sub = 1
    c_eff = 1
    delta = 3

    lambda_0 = 10 ** -4

    c = Core([vf_1, vf_2, vf_3, vf_4], lambda_0, i_sub, c_eff, delta)

    f1 = Fault(220)
    f2 = Fault(450)
    f3 = Fault(660)

    fault_ls = [f1, f2, f3]

    checkpoint_insertion_overhead = 10
    rollback_overhead = 10

    et = 550
    d = 1180


    t = Task(et, len(fault_ls), d, c, fault_ls, 
             checkpoint_insertion_overhead, rollback_overhead)

    def run_bench():

        data = []

        print(BOLD + ("### Starting '%s' ###" % bench_3.__name__) + ENDC)
        print(BOLD + "--- TsCp Begin ---" + ENDC)
        data.append(bench_3.t.run())
        print(BOLD + "--- TsCp End ---" + ENDC)

        print()

        print(BOLD + "--- TsCp-DVS Begin ---" + ENDC)
        data.append(bench_3.t.run_dvs())
        print(BOLD + "--- TsCp-DVS End ---" + ENDC)

        print()

        print(BOLD + "--- Non-Uniform Begin ---" + ENDC)
        data.append(bench_3.t.run_non_uniform())
        print(BOLD + "--- Non-Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Uniform Begin ---" + ENDC)
        data.append(bench_3.t.run_uniform())
        print(BOLD + "--- Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Reliability-Target Begin ---" + ENDC)
        data.append(bench_3.t.run_reliability_taret(0.99999))
        print(BOLD + "--- Reliability-Target End ---" + ENDC)
        print(BOLD + ("### '%s' Finished ###" % bench_3.__name__) + ENDC)

        print()
        return data

BENCH = [bench_1, bench_2, bench_3]