import numpy as np
import matplotlib.pyplot as plt

# Simple script to calculate number of peaks in given csv

class Data(object):
    def __init__(self, times, potentials, temperatures, approx_max):
        self.temperatures = temperatures
        self.times = times
        self.potentials = potentials
        self.approx_max = approx_max


    # packs the data a bit to 'smooth it' out for viewing and
    # so that peak finder can work

    def smooth(self, packing_constant):
        new_times = []
        new_potentials = []
        new_temps = []
        counter = packing_constant
        running_total_temp = 0
        running_total_poten = 0
        for x in range(0, len(self.times)):
            if(counter == 0):
                new_times.append((self.times[x] + self.times[x - packing_constant]) / 2)
                new_potentials.append(running_total_poten/packing_constant)
                new_temps.append(running_total_temp/packing_constant)
                counter = packing_constant
                running_total_poten = 0
                running_total_temp = 0
            else:
                running_total_poten += self.potentials[x]
                running_total_temp += self.temperatures[x]
                counter = counter - 1
        self.times = new_times
        self.potentials = new_potentials
        self.temperatures = new_temps

    # give a **lowballed** approximate max
    # may have unexpected results without smoothed data

    def peak_finder(self):
        total = 0
        b = True
        for x in range(0, len(self.times)):
            if(self.potentials[x] > self.approx_max and b):
                total = total + 1
                b = False
            elif(self.potentials[x] < self.approx_max and not b):
                b = True
        return total


offset = 2128
end = 5825

data = np.loadtxt("trial3.csv", delimiter=',', comments='#',usecols=(0,1,2))
times = data[offset:end:,0]
potentials = data[offset:end:,2]
temperatures = data[offset:end:,1]
d = Data(times,potentials,temperatures, 4)
d.smooth(3)
#plt.plot(d.times, d.potentials)
#plt.plot(d.temperatures, d.potentials)

plt.plot(d.times, d.temperatures)

print(d.peak_finder())
print(temperatures[0] - temperatures[len(temperatures) - 1] )


