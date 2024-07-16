
from math import sqrt, floor, ceil

from Core import Core

# Times are based on micro-seconds

CONST_E_MEM = 0.46

class Fault:
    def __init__(self, time: int):
         self.time = time

    def __repr__(self):
        return "fault(time:%d, persistence:%d)" % (self.time, self.persistence)

    def __str__(self):
        return self.__repr__()

class Non_Uniform_Checkpoint:
    def __init__(self, time:int):
        self.time = time

    def __repr__(self):
        return "non-uniform checkpoint(time:%d)" % self.time

    def __str__(self):
        return self.__repr__()

class Uniform_Checkpoint:
    def __init__(self, time:int):
        self.time = time

    def __repr__(self):
        return "uniform checkpoint(time:%d)" % self.time

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
                #print(n)
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
        print(schemes)

        non_uniforms = list()
        uniforms = list()
        for i in schemes:
            non_uniforms.append(i[0])
            uniforms.append(i[1:])

        FAULTY = False

        last_checkpoint_execution_time = 0
        last_checkpoint = 0
        n_checkpoint = 0
        uniform_index = -1
        #print(non_uniforms)
        #n = self.calculate_n_optu(1, self.execution_time)
        #print(n)
        #print(self.execution_time / n)
        #print(self.calculate_wcet(2, n, self.execution_time))

        print("Task start:")
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
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
                        print("switching to uniform!")
                        last_checkpoint = checkpoint.time
                        BREAKOUT = True
                        break

                    last_checkpoint_execution_time = t
                    last_checkpoint = checkpoint.time

            if BREAKOUT:
                break

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")

        E_ni = d * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM
        d_temp = d
        n_checkpoint = 0

        uniform_scheme = uniforms[uniform_index]
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    FAULTY = True
                    self.faults.remove(fault)

            CONTINUE = False

            for checkpoint in uniform_scheme:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    d += self.checkpoint_insertion
                    print(checkpoint)
                    uniform_scheme.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time
                        FAULTY = False

                    CONTINUE = True

                    last_checkpoint = checkpoint.time
                    last_checkpoint_execution_time = t

                    break

            #print(t, d)

            if CONTINUE:
                continue

            t += 1
            d += 1


        if d > self.deadline:
            raise Exception("Deadline missed!!!")
        else:
            print("Task finished!")
            print("Total execution time: %d" % (d-1))
            E_ui = (d - d_temp) * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM
            print("Power consumption in non-uniform state: %f" % E_ni)
            print("Power consumption in uniform state: %f" % E_ui)
            print("Total power consumption state: %f" % (E_ni + E_ui))

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
        #for i in schemes:
        #    print(i)
        #    print()

        scheme = schemes[0]
        p = scheme[0][1]
        f = scheme[0][2]
        v = scheme[0][3]

        checkpointing_scheme = tuple([ x[0] for x in scheme ])
        print(checkpointing_scheme)

        non_uniforms = list()
        uniforms = list()
        for i in checkpointing_scheme:
            non_uniforms.append(i[0])
            uniforms.append(i[1:])

        FAULTY = False

        last_checkpoint_execution_time = 0
        last_checkpoint = 0
        n_checkpoint = 0
        uniform_index = -1
        #print(non_uniforms)
        #n = self.calculate_n_optu(1, self.execution_time)
        #print(n)
        #print(self.execution_time / n)
        #print(self.calculate_wcet(2, n, self.execution_time))

        print("Task start:")
        print("DVS enabled.")
        while t <= self.execution_time / p and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
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
                        print("switching to uniform!")
                        print("DVS disabled.")
                        last_checkpoint = checkpoint.time
                        BREAKOUT = True
                        break

                    last_checkpoint_execution_time = t
                    last_checkpoint = checkpoint.time

            if BREAKOUT:
                break

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")

        E_ni = (d / p) * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM
        d_temp = d
        n_checkpoint = 0
        t = floor(t * p)

        uniform_scheme = uniforms[uniform_index]
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    FAULTY = True
                    self.faults.remove(fault)

            CONTINUE = False

            for checkpoint in uniform_scheme:
                if checkpoint.time == d:
                    print("checkpoint set!")
                    d += self.checkpoint_insertion
                    print(checkpoint)
                    uniform_scheme.remove(checkpoint)
                    if FAULTY:
                        print("fault detected!!")
                        print("rollback to %d" % last_checkpoint_execution_time)
                        t = last_checkpoint_execution_time
                        FAULTY = False

                    CONTINUE = True

                    last_checkpoint = checkpoint.time
                    last_checkpoint_execution_time = t

                    break

            #print(t, d)

            if CONTINUE:
                continue

            t += 1
            d += 1


        if d > self.deadline:
            raise Exception("Deadline missed!!!")
        else:
            print("Task finished!")
            print("Total execution time: %d" % (d-1))
            v = self.core.voltage_frequency[-1].v
            f = self.core.voltage_frequency[-1].f
            E_ui = (d-d_temp) * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM
            print("Power consumption in non-uniform state: %f" % E_ni)
            print("Power consumption in uniform state: %f" % E_ui)
            print("Total power consumption state: %f" % (E_ni + E_ui))

    def run_non_uniform(self):
        t = 0
        d = 0

        v = self.core.voltage_frequency[-1].v
        f = self.core.voltage_frequency[-1].f

        schemes = self.calculate_all_checkpoint_schemes()

        non_uniforms = list()
        for i in schemes:
            non_uniforms.append(i[0])

        print(non_uniforms)

        FAULTY = False

        last_checkpoint_execution_time = 0
        last_checkpoint = 0
        n_checkpoint = 0
        uniform_index = -1
        #print(non_uniforms)
        #n = self.calculate_n_optu(1, self.execution_time)
        #print(n)
        #print(self.execution_time / n)
        #print(self.calculate_wcet(2, n, self.execution_time))

        print("Task start:")
        print("Non-uniform checkpointing scheme!")
        while t <= self.execution_time and d <= self.deadline:
            if d and d % 100 == 0:
                print("task execution status: (executed time: %d, total time: %d)" % (t, d))

            for fault in self.faults:
                if fault.time == d:
                    print("fault occured!")
                    FAULTY = True
                    self.faults.remove(fault)

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
                        last_checkpoint = checkpoint.time
                        break

                    last_checkpoint_execution_time = t
                    last_checkpoint = checkpoint.time

            t += 1
            d += 1

        if d > self.deadline:
            raise Exception("Deadline missed!!!")

        E_ni = d * self.core.calculate_power_consumption(f, v) + n_checkpoint * CONST_E_MEM

        print("Task finished!")
        print("Total execution time: %d" % (d-1))
        print("Total power consumption state: %f" % E_ni)
