"""
Simple script to produce graphs and plots from
thermal expansion coeffecient lab

@input   CSV file of times, potentials, and temperatures

@output  Plot of potential vs time, temperature vs time,
         and potential vs temperature

@author  owensheekey
"""
import numpy as np
import matplotlib.pyplot as plt



# Data object is a combination of all data from CSV

# @init params
#              - file_name   name of csv
#              - approx_max  above this potential peak will count
#              - start       +ve csv offset
#              - end         last point to include [-1 to include to end]
class Data(object):
    def __init__(self, file_name, approx_max, start, end):
        data = np.loadtxt(file_name, delimiter=',', comments='#',usecols=(0,1,2))
        if(end == -1):
            self.times  = data[start::,0]
            self.temps  = data[start::,1]
            self.potens = data[start::,2]
        else:
            self.times  = data[start:end:,0]
            self.temps  = data[start:end:,1]
            self.potens = data[start:end:,2]
        self.approx_max = approx_max

    # smooth_all packs all 3 arrays by given constant
    def smooth_all(self, packing_constant):
        new_times      = []
        new_potentials = []
        new_temps      = []
        counter = packing_constant
        running_total_temp  = 0
        running_total_poten = 0
        for x in range(0, len(self.times)):
            if(counter == 0):
                new_times     .append((self.times[x] + self.times[x - packing_constant]) / 2)
                new_potentials.append(running_total_poten/packing_constant)
                new_temps     .append(running_total_temp/packing_constant)
                counter = packing_constant
                running_total_poten = 0
                running_total_temp  = 0
            else:
                running_total_poten += self.potens[x]
                running_total_temp  += self.temps[x]
                counter = counter - 1
        self.times = new_times
        self.potens = new_potentials
        self.temps = new_temps

    # new implementation using a more sophisticated n-point smooth

    def smooth_temp(self, roll_length):
        new_arr = []
        rolling_arr = []
        for x in range(0, len(self.times)):
            if(len(rolling_arr) >= roll_length):
                rolling_arr.pop(0)
            rolling_arr.append(self.temps[x])
            new_arr.append(np.mean(rolling_arr))
        self.temps = new_arr

    # Counts and returns # of peaks in potens based on approx_max
    # Unexpected results if data is not smoothed
    def peak_finder(self):
        total = 0
        b     = True
        for x in range(0, len(self.times)):
            if  (self.potens[x] > self.approx_max and b):
                total = total + 1
                b     = False
            elif(self.potens[x] < self.approx_max and not b):
                b     = True
        return total

# End of class definition
# ------------------------------------------------------------------------
# Start of additional function definitions


# Calculates and returns a rough thermal expansion coeffecient
# @param Data object with needed fields
# Laser wavelength:     632.8 nm
# Length of copper bar: 88.00 mm
def calculate_alpha_rough(data):
    num_peaks = data.peak_finder()
    Dtemp     = data.temps[0] - data.temps[len(data.temps) - 1]
    alpha = (num_peaks * 632.8e-9)/ (2 * 88e-3 * Dtemp)
    return alpha

# Graphing functions -- pretty self explanatory
def graph_time_poten(data):
    plt.figure(1)
    plt.plot(data.times, data.potens)
    plt.title ("Potential vs Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Potential (volts)")
    plt.show()

def graph_time_temp(data):
    plt.figure(2)
    plt.plot(data.times, data.temps)
    plt.title ("Temperature vs Time")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Temperature (degrees C)")
    plt.show()

def graph_temp_poten(data):
    plt.figure(3)
    plt.plot(data.temps, data.potens)
    plt.title ("Potential vs Temperature")
    plt.xlabel("Temperature (degrees C)")
    plt.ylabel("Potential (volts)")
    plt.show()

# End of additional function definitions
# ------------------------------------------------------------------------
# All function calls and setup -- You should edit this depending on inputs


data = Data("trial3.csv", 4, 2128, 5825)
data.smooth_all(3)
print("Thermal Expansion Coeffecient, alpha (before temperature smoothing):")
print(calculate_alpha_rough(data))
graph_time_poten(data)
graph_time_temp (data)
data.smooth_temp(20)
graph_time_temp (data)
graph_temp_poten(data)
print("Thermal Expansion Coeffecient, alpha (after temperature smoothing):")
print(calculate_alpha_rough(data))
