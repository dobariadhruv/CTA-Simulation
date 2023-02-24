import MonteCarlo_1 as mc
import numpy.random as rand

# https://www.transitchicago.com/assets/1/6/Monthly_Ridership_2022-10(Final).pdf

stations = ["O'Hare", "Rosemont", "Cumberland", "Harlem", "Jefferson Park", "Montrose", "Irving Park", "Addison",
            "Belmont", "Logan Square", "California", "Western", "Damen", "Division", "Chicago", "Grand", "Clark/Lake",
            "Washington", "Monroe", "Jackson", "LaSalle", "Clinton", "UIC-Halsted", "Racine",
            "Illinois Medical District", "Western", "Kedzie-Homan", "Pulaski", "Cicero", "Austin", "Oak Park", "Harlem",
            "Forest Park"]
entering_passengers = rand.randint(50, 640, size=33)
leaving_passengers = rand.randint(10, 50, size=33)


class TrainSimulation(mc.MonteCarlo):
    def SimulateOnce(self):
        total_passengers = []
        for i in range(33):
            total_passengers.append(entering_passengers[i] - leaving_passengers[i])
        return total_passengers


sim = TrainSimulation()
mean_result = sim.RunSimulation(1000)
total_footfall = sim.results
for j, x in zip(stations, zip(*total_footfall)):
    print("Total Footfall at ",j, " is :", sum(x) / len(x))
