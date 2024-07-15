
I_SUB = 1
C_EFF = 1
DELTA = 1

class Volatage_Frequency:
    def __init__(self, voltage, frequency):
        self.v = voltage
        self.f = frequency
    
    def __repr__(self):
        return "voltage-frequency(%fv, %fGhz)" % (self.v, self.f)
    
    def __str__(self):
        return self.__repr__()

class Core:
    def __init__(self, voltage_frequency:list, initial_fault_rate:float, I_sub:float,C_eff:float,
                 delta:float):
        
        self.voltage_frequency = sorted(voltage_frequency, key=lambda x: x.f)
        self.voltages = [ x.v for x in voltage_frequency ]
        self.initial_fault_rate = initial_fault_rate
        self.operating = voltage_frequency[-1]
        self.I_sub = I_sub
        self.C_eff = C_eff
        self.delta = delta
        
        self.frequency_norm = list()
        freq_temp = list()
        for i in voltage_frequency: # get the operating frequencies and voltages
            freq_temp.append(i.f)

        max_f = max(freq_temp)

        for i in freq_temp: # normalizing frequencies
            self.frequency_norm.append(i / max_f)

    def calculate_power_consumption(self, f, v):
        # based on operating voltage-frequency
        return (self.I_sub * self.operating.v) + \
            (self.C_eff * v * v * f)
    
    def calculate_fault_rate (self):
        return self.initial_fault_rate * 10 ** ((max(self.voltages) - self.operating.v) / self.delta)


    def __repr__(self):
        return "core(operating: %s, voltage-frequency:%s, I_sub:%f, C_eff:%f, delta:%f)" % \
                                                                            (self.operating,
                                                                             self.voltage_frequency,
                                                                             self.I_sub,
                                                                             self.C_eff,
                                                                             self.delta)
    
    def __str__(self):
        return self.__repr__()
    