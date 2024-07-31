from Core import Core, Volatage_Frequency
from Task import Task, Fault
from bcolor import *

class bench_1:
    vf_1 = Volatage_Frequency(1, 1.75)
    vf_2 = Volatage_Frequency(3, 2)

    i_sub = 1
    c_eff = 1
    delta = 3

    lambda_0 = 10 ** -4

    c = Core([vf_1, vf_2], lambda_0, i_sub, c_eff, delta)

    f1 = Fault(90)
    f2 = Fault(450)

    fault_ls = [f1, f2]

    checkpoint_insertion_overhead = 10
    rollback_overhead = 10
    et = 420

    util = 0.3
    d = round(et / util)


    t = Task(et, len(fault_ls), d, c, fault_ls, 
             checkpoint_insertion_overhead, rollback_overhead)

    def run_bench():

        data = []

        print(BOLD + ("### Starting '%s' ###" % bench_1.__name__) + ENDC)
        print(BOLD + "Utilization: %{}".format(bench_1.util * 100) + ENDC)
        print(BOLD + "Deadline: {}".format(bench_1.d) + ENDC)
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
        data.append(bench_1.t.run_reliability_target(0.99999))
        print(BOLD + "--- Reliability-Target End ---" + ENDC)
        print(BOLD + ("### '%s' Finished ###" % bench_1.__name__) + ENDC)

        print()
        return data
    
class bench_2:
    vf_1 = Volatage_Frequency(1, 1.75)
    vf_2 = Volatage_Frequency(3, 2)

    i_sub = 1
    c_eff = 1
    delta = 3

    lambda_0 = 10 ** -4

    c = Core([vf_1, vf_2], lambda_0, i_sub, c_eff, delta)

    f1 = Fault(90)
    f2 = Fault(450)

    fault_ls = [f1, f2]

    checkpoint_insertion_overhead = 10
    rollback_overhead = 10
    et = 420

    util = 0.4
    d = round(et / util)


    t = Task(et, len(fault_ls), d, c, fault_ls, 
             checkpoint_insertion_overhead, rollback_overhead)

    def run_bench():

        data = []

        print(BOLD + ("### Starting '%s' ###" % bench_2.__name__) + ENDC)
        print(BOLD + "Utilization: %{}".format(bench_2.util * 100) + ENDC)
        print(BOLD + "Deadline: {}".format(bench_2.d) + ENDC)
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
        data.append(bench_2.t.run_reliability_target(0.99999))
        print(BOLD + "--- Reliability-Target End ---" + ENDC)
        print(BOLD + ("### '%s' Finished ###" % bench_2.__name__) + ENDC)

        print()
        return data
    
class bench_3:
    vf_1 = Volatage_Frequency(1, 1.75)
    vf_2 = Volatage_Frequency(3, 2)

    i_sub = 1
    c_eff = 1
    delta = 3

    lambda_0 = 10 ** -4

    c = Core([vf_1, vf_2], lambda_0, i_sub, c_eff, delta)

    f1 = Fault(90)
    f2 = Fault(450)

    fault_ls = [f1, f2]

    checkpoint_insertion_overhead = 10
    rollback_overhead = 10
    et = 420

    util = 0.5
    d = round(et / util)


    t = Task(et, len(fault_ls), d, c, fault_ls, 
             checkpoint_insertion_overhead, rollback_overhead)

    def run_bench():

        data = []

        print(BOLD + ("### Starting '%s' ###" % bench_3.__name__) + ENDC)
        print(BOLD + "Utilization: %{}".format(bench_3.util * 100) + ENDC)
        print(BOLD + "Deadline: {}".format(bench_3.d) + ENDC)
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
        data.append(bench_3.t.run_reliability_target(0.99999))
        print(BOLD + "--- Reliability-Target End ---" + ENDC)
        print(BOLD + ("### '%s' Finished ###" % bench_3.__name__) + ENDC)

        print()
        return data
    
class bench_4:
    vf_1 = Volatage_Frequency(1, 1.75)
    vf_2 = Volatage_Frequency(3, 2)

    i_sub = 1
    c_eff = 1
    delta = 3

    lambda_0 = 10 ** -4

    c = Core([vf_1, vf_2], lambda_0, i_sub, c_eff, delta)

    f1 = Fault(90)
    f2 = Fault(450)

    fault_ls = [f1, f2]

    checkpoint_insertion_overhead = 10
    rollback_overhead = 10
    et = 420

    util = 0.6
    d = round(et / util)


    t = Task(et, len(fault_ls), d, c, fault_ls, 
             checkpoint_insertion_overhead, rollback_overhead)
    
    def run_bench():

        data = []

        print(BOLD + ("### Starting '%s' ###" % bench_4.__name__) + ENDC)
        print(BOLD + "Utilization: %{}".format(bench_4.util * 100) + ENDC)
        print(BOLD + "Deadline: {}".format(bench_4.d) + ENDC)
        print(BOLD + "--- TsCp Begin ---" + ENDC)
        data.append(bench_4.t.run())
        print(BOLD + "--- TsCp End ---" + ENDC)

        print()

        print(BOLD + "--- TsCp-DVS Begin ---" + ENDC)
        data.append(bench_4.t.run_dvs())
        print(BOLD + "--- TsCp-DVS End ---" + ENDC)

        print()

        print(BOLD + "--- Non-Uniform Begin ---" + ENDC)
        data.append(bench_4.t.run_non_uniform())
        print(BOLD + "--- Non-Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Uniform Begin ---" + ENDC)
        data.append(bench_4.t.run_uniform())
        print(BOLD + "--- Uniform End ---" + ENDC)

        print()

        print(BOLD + "--- Reliability-Target Begin ---" + ENDC)
        data.append(bench_4.t.run_reliability_target(0.99999))
        print(BOLD + "--- Reliability-Target End ---" + ENDC)
        print(BOLD + ("### '%s' Finished ###" % bench_4.__name__) + ENDC)

        print()
        return data

BENCH = [bench_1, bench_2, bench_3, bench_4]