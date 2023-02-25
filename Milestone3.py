import numpy.random as rand
import numpy as np

# https://www.transitchicago.com/assets/1/6/Monthly_Ridership_2022-10(Final).pdf


class MonteCarlo:
    """
    The SimulateOnce method is declared as abstract (it doesn't have an implementation
    in the base class) that must be extended/overriden to build the simualtion.
    """
    
    def SimulateOnce(self):
        raise NotImplementedError
        
    def bootstrap(self, x, confidence=.68, nSamples=100):
        # Make "nSamples" new datasets by re-sampling x with replacement
        # the size of the samples should be the same as x itself
        means = []
        for k in range(nSamples):
            sample = np.random.choice(x, size=len(x), replace=True)
            means.append(np.mean(sample))
        means.sort()
        leftTail = int(((1.0 - confidence)/2) * nSamples)
        rightTail = (nSamples - 1) - leftTail
        return means[leftTail], np.mean(x), means[rightTail]
    
    # This function computes the value at risk amount for the results of a simulation
    # It can only be run after the main simulation is run, so in this function we
    # test for whether the results member exists and if not, print an error    
    def var(self, risk = .05):
        if hasattr(self, "results"):               # See if the results have been calculated 
            self.results.sort()                    # Sort them
            index = int(len(self.results)*risk)    # Count them and multiply by the risk factor  
            return(self.results[index])            # Return the value at that index
        else:
            print("RunSimulation must be executed before the method 'var'")
            return 0.0

    # This function runs the simulation.  Note that it stores the results of each of the
    # trials in an array that is a CLASS variable, not a local variable in this function
    # so, we can get this array from the MonteCarlo object after running if we wish,
    # and we can also call the "var" method as well
    def RunSimulation(self, simCount=10000):
        self.results = []       # Array to hold the results
        
        # Now, we set up the simulation loop
        self.convergence = False
        for k in range(simCount):   
            x = self.SimulateOnce()     # Run the simulation
            self.results.append(x)      # Add the result to the array
                
        return self.bootstrap(self.results)


stations = ["O'Hare", "Rosemont", "Cumberland", "Harlem", "Jefferson Park", "Montrose", "Irving Park", "Addison",
            "Belmont", "Logan Square", "California", "Western", "Damen", "Division", "Chicago", "Grand", "Clark/Lake",
            "Washington", "Monroe", "Jackson", "LaSalle", "Clinton", "UIC-Halsted", "Racine",
            "Illinois Medical District", "Western", "Kedzie-Homan", "Pulaski", "Cicero", "Austin", "Oak Park", "Harlem",
            "Forest Park"]


class TrainSimulation(mc.MonteCarlo):
    def __init__(self, stations, num_trains):
        self.stations = stations
        self.station_traffic = {}
        self.num_trains = num_trains

        for station in self.stations:
            self.station_traffic[station] = 0



    def SimulateOneTrain(self):
        # Generating Riders
        riders_in_stations = rand.normal(4313 / self.num_trains, (0.67*4313) / self.num_trains, 33)

        # Minimum of 0 riders, as opposed to negative riders.
        for i in range(len(riders_in_stations)):
            if riders_in_stations[i] <= 0:
                riders_in_stations[i] = 0

        # Tracking Destinations
        rider_destinations = {}
        for station in self.stations:
            rider_destinations[station] = 0
            
        # Tracking people on the train
        people_on_train = 0

        # Iterate through stations
        for i in range(len(self.stations)):
            # Figure out possible destinations for new riders
            possible_destinations = self.stations[i + 1:]

            # Distribute new riders to all possible destinations
            for destination in possible_destinations:
                rider_destinations[destination] += riders_in_stations[i] / len(possible_destinations)

            # Add new riders to train
            people_on_train += riders_in_stations[i]
            
            # Remove people getting off the train at this destination
            people_on_train -= rider_destinations[self.stations[i]]

        total_riders = sum(riders_in_stations)
        total_exits = sum(rider_destinations.values())

        riders_per_station = total_riders / len(self.stations)

        return riders_per_station

            
    def SimulateOnce(self):

        rps_per_day = 0

        for i in range(self.num_trains):
            rps_per_day += self.SimulateOneTrain()

        return rps_per_day




sim1 = TrainSimulation(stations, 200)
sim1.SimulateOnce()
sim1.RunSimulation(1000)


# our numbers are based on daily total ridership. that's very different from one train going from one end of the Blue Line to the other--with no returns.
# SO we also need to figure out how many trains run in a day -- turns out to be 200, going each direction
# AND sometimes trains only travel partway down the line -- that's for later