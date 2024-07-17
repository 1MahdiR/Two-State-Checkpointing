from bcolor import *

I_SUB = 1
C_EFF = 1
DELTA = 3

class Volatage_Frequency:
    def __init__(self, voltage, frequency):
        self.v = voltage
        self.f = frequency

    def __repr__(self):
        return WARNING + ("voltage-frequency(%fv, %fGhz)" % (self.v, self.f)) + ENDC

    def __str__(self):
        return self.__repr__()

class Core:
    def __init__(self, voltage_frequency:list, initial_fault_rate:float, I_sub:float,C_eff:float,
                 delta:float):

        self.voltage_frequency = sorted(voltage_frequency, key=lambda x: x.f)
        self.voltages = [ x.v for x in voltage_frequency ]
        self.initial_fault_rate = initial_fault_rate
        self.I_sub = I_sub
        self.C_eff = C_eff
        self.delta = delta

    def calculate_power_consumption(self, f, v):
        return (self.I_sub * v) + \
            (self.C_eff * v * v * f)

    def calculate_fault_rate (self, v):
        return self.initial_fault_rate * 10 ** ((max(self.voltages) - v) / self.delta)


    def __repr__(self):
        return WARNING + ("core(voltage-frequency:%s, I_sub:%f, C_eff:%f, delta:%f)" % \
                                                                            (self.voltage_frequency,
                                                                             self.I_sub,
                                                                             self.C_eff,
                                                                             self.delta)) + ENDC

    def __str__(self):
        return self.__repr__()
