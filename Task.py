from math import sqrt, floor, ceil, factorial
from math import e as e_num

from Core import Core
from bcolor import *

CONST_E_MEM = 4.6

class Fault:
    def __init__(self, time: int):
         self.time = time

    def __repr__(self):
        return FAIL + ("fault(time:%d)" % (self.time)) + ENDC

    def __str__(self):
        return self.__repr__()

class Non_Uniform_Checkpoint:
    def __init__(self, time:int):
        self.time = time

    def __repr__(self):
        return WARNING + ("non-uniform checkpoint(time:%d)" % self.time) + ENDC

    def __str__(self):
        return self.__repr__()

class Uniform_Checkpoint:
    def __init__(self, time:int):
        self.time = time

    def __repr__(self):
        return WARNING + ("uniform checkpoint(time:%d)" % self.time) + ENDC

    def __str__(self):
        return self.__repr__()

class Task:
    def __init__(self, execution_time:int, tolerable_faults:int, deadline:int, core:Core, faults:list,
                 checkpoint_insertion:int, rollback:int):
        self.execution_time = execution_time
        self.tolerable_faults = tolerable_faults
        self.deadline = deadline
        self.core = core
        self.utilization = execution_time / deadline
        self.faults = sorted(faults, key=lambda x: x.time)
        self.checkpoint_insertion = checkpoint_insertion
        self.rollback = rollback

        self.checkpoints = []

    def calculate_reliability(self, k, v, f, n, et=None):
        f_max = self.core.voltage_frequency[-1].f
        p = f / f_max

        if et == None:
            et = self.execution_time / p

        fault_rate = self.core.calculate_fault_rate(v)

        if n == 0:
            WCET = et
        else:
            WCET = self.calculate_wcet(k, n, et)
        
        R = 0
        for i in range(k+1):
            top = ((fault_rate * WCET) ** i) * (e_num ** (-fault_rate * WCET))
            bottom = factorial(i)

            R += top / bottom

        return R

    def calculate_n_optu(self, tolerable_faults, execution_time):
        k = tolerable_faults
        t = execution_time
        c = self.checkpoint_insertion

        n_minus = floor(sqrt((k*t)/c))
        n_plus = ceil(sqrt((k*t)/c))

        if c * ((n_minus * (n_minus + 1))/k) >= t:
            return n_minus
        else:
            return n_plus

    def calculate_wcet(self, tolerable_faults, number_of_checkpoints, execution_time):
        k = tolerable_faults
        n = number_of_checkpoints
        t = execution_time
        c = self.checkpoint_insertion
        r = self.rollback

        return t + n * c + k * (r + (t // n))
    
    def calculate_uniform_checkpoint_scheme(self):
        n_optu = self.calculate_n_optu(self.tolerable_faults, self.execution_time)
        scheme = list()

        ui = self.execution_time // n_optu

        t = ui
        scheme.append(Uniform_Checkpoint(ui))
        t += ui + self.checkpoint_insertion
        n_optu -= 1

        while t < self.deadline and n_optu:
            scheme.append(Uniform_Checkpoint(t))
            t += ui + self.checkpoint_insertion
            n_optu -= 1
        
        return scheme

    def calculate_checkpoint_scheme(self, time, interval, number_of_uniform_checkpoints):
        scheme = list()

        scheme.append(Non_Uniform_Checkpoint(time))
        time += interval + self.checkpoint_insertion

        while time < self.deadline and number_of_uniform_checkpoints:
            scheme.append(Uniform_Checkpoint(time))
            time += interval + self.checkpoint_insertion
            number_of_uniform_checkpoints -= 1

        return scheme

    def calculate_all_checkpoint_schemes(self):
        t = self.execution_time
        d = self.deadline
        c = self.checkpoint_insertion
        r = self.rollback
        k = self.tolerable_faults

        schemes = list()
        shift = 0

        if k == 1:
            while t > 0:
                ui = t
                ni = floor(d - (r + t + c))

                if ni >= t:
                    schemes.append(self.calculate_checkpoint_scheme(shift + t - c, ui, 999999))
                    break
                else:
                    schemes.append(self.calculate_checkpoint_scheme(ni + shift, ui, 999999))

                if ni <= 0:
                    raise Exception("Infeasible!!!")

                d = d - ni - c
                t = t - ni
                shift = shift + ni + c
        else:
            while t > 0:
                n = self.calculate_n_optu(k-1, t)
                ni = floor(d - (r + self.calculate_wcet(k-1, n, t)))
                ui = t // n

                if ni >= t:
                    schemes.append(self.calculate_checkpoint_scheme(shift + t, ui, n))
                    break
                else:
                    schemes.append(self.calculate_checkpoint_scheme(ni + shift, ui, n))

                if ni <= 0:
                    raise Exception("Infeasible!!!")

                d = d - ni - c
                t = t - ni
                shift = shift + ni + c

        return schemes

    def run(self):
        t = 0
        d = 0

        v = self.core.voltage_frequency[-1].v
        f = self.core.voltage_frequency[-1].f

        schemes = self.calculate_all_checkpoint_schemes()
        print("All checkpointing schemes:")
        for item in schemes:
            print(item)
        print()

        non_uniforms = list()
        uniforms = list()
        for i in schemes:
            non_uniforms.append(i[0])
            uniforms.append(i[1:])

        FAULTY = False

        last_checkpoint_execution_time = 0
        n_checkpoint = 0
        uniform_index = -1

        print(OKGREEN + "Task start:" + ENDC)
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    print(fault)
                    FAULTY = True
                    self.faults.remove(fault)

            BREAKOUT = False

            for checkpoint in non_uniforms:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    n_checkpoint += 1
                    d += self.checkpoint_insertion
                    print(checkpoint)
                    uniform_index = non_uniforms.index(checkpoint)

                    non_uniforms.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time

                        FAULTY = False

                        t += 1
                        d += 1
                        print(WARNING + "switching to uniform!" + ENDC)
                        BREAKOUT = True
                        break

                    last_checkpoint_execution_time = t

            if BREAKOUT:
                break

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")

        E_ni = d * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM
        d_temp = d
        n_checkpoint_ui = 0

        uniform_scheme = uniforms[uniform_index]
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    print(fault)
                    FAULTY = True
                    self.faults.remove(fault)

            CONTINUE = False

            for checkpoint in uniform_scheme:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    d += self.checkpoint_insertion
                    print(checkpoint)
                    n_checkpoint_ui += 1
                    uniform_scheme.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time
                        FAULTY = False

                    CONTINUE = True

                    last_checkpoint_execution_time = t

                    break

            if CONTINUE:
                continue

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")
        else:
            print()
            print(OKGREEN + BOLD + "Task finished!" + ENDC)
            print(OKGREEN + BOLD + "--------------" + ENDC)
            print("Total execution time: %d" % (d-1))
            E_ui = (d - d_temp) * self.core.calculate_power_consumption(f, v) + n_checkpoint_ui * CONST_E_MEM
            print("Power consumption in non-uniform state: %f" % E_ni)
            print("Power consumption in uniform state: %f" % E_ui)
            print("Total power consumption state: %f" % (E_ni + E_ui))
            R = self.calculate_reliability(self.tolerable_faults, v, f, n_checkpoint_ui + n_checkpoint)
            print("Reliability: %f" % R)

    def calculate_scheme_energy(self, scheme, p, f, v):
        return ((self.execution_time + len(scheme) * self.checkpoint_insertion) / p) * self.core.calculate_power_consumption(f, v) + len(scheme) * CONST_E_MEM

    def calculate_all_checkpoint_schemes_with_best_dvs(self):

        all_schemes = list()
        for voltage_frequency in self.core.voltage_frequency:
            FEASIBLE = True
            schemes = list()

            p = voltage_frequency.f / self.core.voltage_frequency[-1].f

            t = self.execution_time
            d = self.deadline
            c = self.checkpoint_insertion
            r = self.rollback
            k = self.tolerable_faults

            shift = 0

            if k == 1:
                while t > 0:
                    ui = t
                    ni = floor(p * (d - (r + t + c)))

                    if ni >= t:
                        scheme = self.calculate_checkpoint_scheme(shift + t - c, ui, 999999)
                        schemes.append((scheme, p, voltage_frequency.f, voltage_frequency.v,
                                        self.calculate_scheme_energy(scheme, p, voltage_frequency.f, voltage_frequency.v)))
                        break
                    else:
                        scheme = self.calculate_checkpoint_scheme(ni + shift, ui, 999999)
                        schemes.append((scheme, p, voltage_frequency.f, voltage_frequency.v,
                                        self.calculate_scheme_energy(scheme, p, voltage_frequency.f, voltage_frequency.v)))

                    if ni <= 0:
                        FEASIBLE = False
                        break

                    d = d - (ni - c)/p
                    t = t - ni
                    shift = shift + ni + c
            else:
                while t > 0:
                    n = self.calculate_n_optu(k-1, t)
                    ni = floor(p * (d - (r + self.calculate_wcet(k-1, n, t))))
                    ui = t // n

                    if ni >= t:
                        scheme = self.calculate_checkpoint_scheme(shift + t, ui, n)
                        schemes.append((scheme, p, voltage_frequency.f, voltage_frequency.v,
                                        self.calculate_scheme_energy(scheme, p, voltage_frequency.f, voltage_frequency.v)))
                        break
                    else:
                        scheme = self.calculate_checkpoint_scheme(ni + shift, ui, n)
                        schemes.append((scheme, p, voltage_frequency.f, voltage_frequency.v,
                                        self.calculate_scheme_energy(scheme, p, voltage_frequency.f, voltage_frequency.v)))

                    if ni <= 0:
                        FEASIBLE = True
                        break

                    d = d - (ni - c)/p
                    t = t - ni
                    shift = shift + ni + c

            if FEASIBLE:
                all_schemes.append(schemes)

        if all_schemes:
            return all_schemes
        raise Exception("Infeasible!!!")

    def run_dvs(self):
        t = 0
        d = 0

        schemes = self.calculate_all_checkpoint_schemes_with_best_dvs()

        scheme = schemes[0]
        p = scheme[0][1]
        f = scheme[0][2]
        v = scheme[0][3]

        checkpointing_scheme = tuple([ x[0] for x in scheme ])
        print("All checkpointing schemes:")
        for item in checkpointing_scheme:
            print(item)
        print()

        non_uniforms = list()
        uniforms = list()
        for i in checkpointing_scheme:
            non_uniforms.append(i[0])
            uniforms.append(i[1:])

        FAULTY = False

        last_checkpoint_execution_time = 0
        n_checkpoint = 0
        uniform_index = -1

        print(OKGREEN + "Task start:" + ENDC)
        print(WARNING + "DVS enabled." + ENDC)
        while t <= self.execution_time / p and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    print(fault)
                    FAULTY = True
                    self.faults.remove(fault)

            BREAKOUT = False

            for checkpoint in non_uniforms:
                if checkpoint.time == d:

                    print("checkpoint set!")
                    n_checkpoint += 1
                    d += round(self.checkpoint_insertion / p)
                    print(checkpoint)
                    uniform_index = non_uniforms.index(checkpoint)
                    non_uniforms.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time

                        FAULTY = False

                        t += 1
                        d += 1
                        print(WARNING + "switching to uniform!" + ENDC)
                        print(WARNING + "DVS disabled." + ENDC)
                        BREAKOUT = True
                        break

                    last_checkpoint_execution_time = t

            if BREAKOUT:
                break

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")

        E_ni = (d / p) * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM
        d_temp = d
        n_checkpoint_ui = 0
        R1 = self.calculate_reliability(1, v, f, n_checkpoint, t)
        t = floor(t * p)
        t_tmp = t

        uniform_scheme = uniforms[uniform_index]
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    print(fault)
                    FAULTY = True
                    self.faults.remove(fault)

            CONTINUE = False

            for checkpoint in uniform_scheme:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    d += self.checkpoint_insertion
                    print(checkpoint)
                    n_checkpoint_ui += 1
                    uniform_scheme.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time
                        FAULTY = False

                    CONTINUE = True

                    last_checkpoint_execution_time = t

                    break

            if CONTINUE:
                continue

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")
        else:
            print()
            print(OKGREEN + BOLD + "Task finished!" + ENDC)
            print(OKGREEN + BOLD + "--------------" + ENDC)
            print("Total execution time: %d" % (d-1))
            v_tmp, f_tmp = v, f
            v = self.core.voltage_frequency[-1].v
            f = self.core.voltage_frequency[-1].f
            E_ui = (d-d_temp) * self.core.calculate_power_consumption(f, v) + (n_checkpoint + n_checkpoint_ui) * CONST_E_MEM
            print("Power consumption in non-uniform state: %f" % E_ni)
            print("Power consumption in uniform state: %f" % E_ui)
            print("Total power consumption state: %f" % (E_ni + E_ui))
            R2 = self.calculate_reliability(self.tolerable_faults-1, v_tmp, f_tmp, n_checkpoint_ui, t-t_tmp)
            print("Reliability: %f" % (R1 * R2))

    def run_non_uniform(self):
        t = 0
        d = 0

        v = self.core.voltage_frequency[-1].v
        f = self.core.voltage_frequency[-1].f

        schemes = self.calculate_all_checkpoint_schemes()
        
        non_uniforms = list()
        for i in schemes:
            non_uniforms.append(i[0])

        print("Checkpointing scheme:")
        print(non_uniforms)
        print()

        FAULTY = False

        last_checkpoint_execution_time = 0
        n_checkpoint = 0

        print(OKGREEN + "Task start:" + ENDC)
        print("Non-uniform checkpointing scheme!")
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    print(fault)
                    FAULTY = True
                    self.faults.remove(fault)

            for checkpoint in non_uniforms:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    n_checkpoint += 1
                    d += self.checkpoint_insertion
                    print(checkpoint)

                    non_uniforms.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time

                        FAULTY = False

                        t += 1
                        d += 1
                        break

                    last_checkpoint_execution_time = t

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")

        E_ni = d * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM

        print()
        print(OKGREEN + BOLD + "Task finished!" + ENDC)
        print(OKGREEN + BOLD + "--------------" + ENDC)
        print("Total execution time: %d" % (d-1))
        print("Total power consumption state: %f" % E_ni)
        R = self.calculate_reliability(self.tolerable_faults, v, f, n_checkpoint)
        print("Reliability: %f" % R)

    def run_uniform(self):
        t = 0
        d = 0

        v = self.core.voltage_frequency[-1].v
        f = self.core.voltage_frequency[-1].f

        scheme = self.calculate_uniform_checkpoint_scheme()
        print("Checkpointing scheme:")
        print(scheme)
        print()

        FAULTY = False

        last_checkpoint_execution_time = 0
        n_checkpoint = 0

        print(OKGREEN + "Task start:" + ENDC)
        print("Uniform checkpointing scheme!")
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    print(fault)
                    FAULTY = True
                    self.faults.remove(fault)

            for checkpoint in scheme:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    n_checkpoint += 1
                    d += self.checkpoint_insertion
                    print(checkpoint)

                    scheme.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time

                        FAULTY = False

                        t += 1
                        d += 1
                        break

                    last_checkpoint_execution_time = t

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")

        E_ui = d * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM

        print()
        print(OKGREEN + BOLD + "Task finished!" + ENDC)
        print(OKGREEN + BOLD + "--------------" + ENDC)
        print("Total execution time: %d" % (d-1))
        print("Total power consumption state: %f" % E_ui)
        R = self.calculate_reliability(self.tolerable_faults, v, f, n_checkpoint)
        print("Reliability: %f" % R)

    def find_minimum_k(self, R_target, v, f):
        R = 0
        k = 0
        p = f / self.core.voltage_frequency[-1].f
        et = self.execution_time / p
        while True:
            if k == 0:
                n_optu = 0
            else:
                n_optu = self.calculate_n_optu(k, et)

            R = self.calculate_reliability(k, v, f, n_optu)

            if R >= R_target:
                break

            k += 1
            
        return k
    
    def run_reliability_taret(self, R_target):
        t = 0
        d = 0

        v = self.core.voltage_frequency[-1].v
        f = self.core.voltage_frequency[-1].f

        k = self.find_minimum_k(R_target, v, f)
        k_tmp = self.tolerable_faults
        self.tolerable_faults = k

        schemes = self.calculate_all_checkpoint_schemes()
        print("All checkpointing schemes:")
        for item in schemes:
            print(item)
        print()

        non_uniforms = list()
        uniforms = list()
        for i in schemes:
            non_uniforms.append(i[0])
            uniforms.append(i[1:])

        FAULTY = False

        last_checkpoint_execution_time = 0
        n_checkpoint = 0
        uniform_index = -1

        print(OKGREEN + "Task start:" + ENDC)
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    print(fault)
                    FAULTY = True
                    self.faults.remove(fault)

            BREAKOUT = False

            for checkpoint in non_uniforms:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    n_checkpoint += 1
                    d += self.checkpoint_insertion
                    print(checkpoint)
                    uniform_index = non_uniforms.index(checkpoint)

                    non_uniforms.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time

                        FAULTY = False

                        t += 1
                        d += 1
                        print(WARNING + "switching to uniform!" + ENDC)
                        BREAKOUT = True
                        break

                    last_checkpoint_execution_time = t

            if BREAKOUT:
                break

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")

        E_ni = d * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM
        d_temp = d
        n_checkpoint_ui = 0

        uniform_scheme = uniforms[uniform_index]
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    print(fault)
                    FAULTY = True
                    self.faults.remove(fault)

            CONTINUE = False

            for checkpoint in uniform_scheme:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    d += self.checkpoint_insertion
                    print(checkpoint)
                    n_checkpoint_ui += 1
                    uniform_scheme.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time
                        FAULTY = False

                    CONTINUE = True

                    last_checkpoint_execution_time = t

                    break

            if CONTINUE:
                continue

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")
        else:
            print()
            print(OKGREEN + BOLD + "Task finished!" + ENDC)
            print(OKGREEN + BOLD + "--------------" + ENDC)
            print("Total execution time: %d" % (d-1))
            E_ui = (d - d_temp) * self.core.calculate_power_consumption(f, v) + n_checkpoint_ui * CONST_E_MEM
            print("Power consumption in non-uniform state: %f" % E_ni)
            print("Power consumption in uniform state: %f" % E_ui)
            print("Total power consumption state: %f" % (E_ni + E_ui))
            R = self.calculate_reliability(self.tolerable_faults, v, f, n_checkpoint_ui + n_checkpoint)
            print("Reliability: %f" % R)
        self.tolerable_faults = k_tmp
