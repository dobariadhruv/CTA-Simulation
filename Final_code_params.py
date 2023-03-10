import numpy as np
import numpy.random as rand


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
        leftTail = int(((1.0 - confidence) / 2) * nSamples)
        rightTail = (nSamples - 1) - leftTail
        return means[leftTail], np.mean(x), means[rightTail]

    # This function computes the value at risk amount for the results of a simulation
    # It can only be run after the main simulation is run, so in this function we
    # test for whether the results member exists and if not, print an error
    def var(self, risk=.05):
        if hasattr(self, "results"):  # See if the results have been calculated
            self.results.sort()  # Sort them
            index = int(len(self.results) * risk)  # Count them and multiply by the risk factor
            return (self.results[index])  # Return the value at that index
        else:
            print("RunSimulation must be executed before the method 'var'")
            return 0.0

    # This function runs the simulation.  Note that it stores the results of each of the
    # trials in an array that is a CLASS variable, not a local variable in this function
    # so, we can get this array from the MonteCarlo object after running if we wish,
    # and we can also call the "var" method as well
    def RunSimulation(self, simCount=10000):
        self.results = []  # Array to hold the results

        # Now, we set up the simulation loop
        self.convergence = False
        for k in range(simCount):
            x = self.SimulateOnce()  # Run the simulation
            self.results.append(x)  # Add the result to the array

        return self.bootstrap(self.results)


stations = np.array([("Addison-O'Hare", 2455, 917),
            ("Austin-Forest Park", 1629, 605),
            ("Belmont-O'Hare", 4532, 1447),
            ("California/Milwaukee", 4609, 1421),
            ("Chicago/Milwaukee", 3469, 1269),
            ("Cicero-Forest Park", 1220, 307),
            ("Clark/Lake", 16359, 7331),
            ("Clinton-Forest Park", 3020, 1196),
            ("Cumberland", 3750, 1387),
            ("Damen/Milwaukee", 5865, 1463),
            ("Division/Milwaukee", 5153, 1749),
            ("Forest Park", 2854, 998),
            ("Grand/Milwaukee", 2375, 722),
            ("Harlem-Forest Park", 1020, 348),
            ("Medical Center", 2278, 1134),
            ("Irving Park-O'Hare", 3694, 1130),
            ("Jackson/Dearborn", 6026, 2466),
            ("Jefferson Park", 5647, 1807),
            ("Kedzie-Homan-Forest Park", 1835, 489),
            ("LaSalle", 2529, 1002),
            ("Logan Square", 6271, 1859),
            ("Monroe/Dearborn", 6310, 2868),
            ("Montrose-O'Hare", 2141, 767),
            ("O'Hare Airport", 10832, 2082),
            ("Oak Park-Forest Park", 1466, 621),
            ("Pulaski-Forest Park", 1615, 297),
            ("Racine", 1843, 772),
            ("Rosemont", 5598, 1685),
            ("UIC-Halsted", 4686, 2737),
            ("Washington/Dearborn", 10718, 3669),
            ("Western-Forest Park", 1421, 424),
            ("Western/Milwaukee", 4496, 1564)])




class TrainSimulation(MonteCarlo):
    def __init__(self, stations, num_trains, weather, big_events):
        self.stations = stations
        self.num_trains = num_trains
        self.weather = weather
        self.big_events = big_events


    def SimulateOneTrain(self):
        # Generating riders based on station distributions
        riders_in_stations = []

        for station in self.stations:
            avg, s_dev = int(station[1]), int(station[2])
            # Create number of riders in the day
            daily_num = rand.normal(avg, s_dev)
            
            if self.weather == 'inclement':
                daily_num *= 0.8
            elif self.weather == 'sunny':
                daily_num *= 1.5
            
            # Adjust riders for big events
            if self.big_events == 'True':
                daily_num *= 1.6
            
            
            # Divide by number of trains that are sent through the day
            riders_in_stations.append(int(daily_num / self.num_trains))

        # Setting station riders to a minimum of 0, to avoid negative riders on a platform
        for i in range(len(riders_in_stations)):
            if riders_in_stations[i] <= 0:
                riders_in_stations[i] = 0

        # Tracking Destinations
        rider_destinations = {}
        for station in self.stations:
            rider_destinations[station[0]] = 0

        # Tracking people on the train
        people_on_train = 0

        # Iterate through stations
        # From O'Hare to Forest Park
        for i in range(len(self.stations)):

            # Remove people getting off the train at this destination
            people_on_train -= rider_destinations[self.stations[i][0]]
            rider_destinations[self.stations[i][0]] = 0

            # Add new riders to train
            new_passengers = riders_in_stations[i]
            people_on_train += new_passengers
            riders_in_stations[i] = 0

            # If the train is at capacity, we can't have everyone on board
            if people_on_train > 640:
                overflow = people_on_train - 640
                new_passengers -= overflow
                riders_in_stations[i] += overflow
                people_on_train = 640

            # Distribute new riders to all possible destinations

            # Figure out possible destinations for new riders
            possible_destinations = len(self.stations[i:])
            index_start = len(rider_destinations) - possible_destinations - 1
            destination_index = index_start

            while new_passengers > 0:
                station_name = self.stations[destination_index][0]
                rider_destinations[station_name] += 1
                new_passengers -= 1
                destination_index += 1

                if destination_index == len(rider_destinations) - 1:
                    destination_index = index_start

        # print(rider_destinations)

        return sum(riders_in_stations)


    def SimulateOneTrainReverse(self):
        # Generating riders based on station distributions
        riders_in_stations = []

        for station in self.stations:
            avg, s_dev = int(station[1]), int(station[2])
            # Create number of riders in the day
            daily_num = rand.normal(avg, s_dev)
            # Divide by number of trains that are sent through the day
            riders_in_stations.append(int(daily_num / self.num_trains))


        # Setting station riders to a minimum of 0, to avoid negative riders on a platform
        for i in range(len(riders_in_stations)):
            if riders_in_stations[i] <= 0:
                riders_in_stations[i] = 0

        # Tracking Destinations
        rider_destinations = {}
        for station in self.stations:
            rider_destinations[station[0]] = 0

        # Tracking people on the train
        people_on_train = 0

        # Iterate through stations
        # From O'Hare to Forest Park
        for i in range(len(self.stations) - 1, -1, -1):

            # Remove people getting off the train at this destination
            people_on_train -= rider_destinations[self.stations[i][0]]
            rider_destinations[self.stations[i][0]] = 0

            # Add new riders to train
            people_on_train += riders_in_stations[i]
            new_passengers = riders_in_stations[i]
            riders_in_stations[i] = 0

            # If the train is at capacity, we can't have everyone on board
            if people_on_train > 640:
                overflow = people_on_train - 640
                new_passengers -= overflow
                riders_in_stations[i] += overflow
                people_on_train = 640

            # Distribute new riders to all possible destinations

            # Figure out possible destinations for new riders
            index_start = i - 1
            destination_index = index_start

            while new_passengers > 0:
                station_name = self.stations[destination_index][0]
                rider_destinations[station_name] += 1
                new_passengers -= 1
                destination_index -= 1

                if destination_index <= 0:
                    destination_index = index_start

        return sum(riders_in_stations)


    def SimulateOnce(self):
        riders = 0
        reverse = 0
        for i in range(self.num_trains):
            riders += self.SimulateOneTrain()
            reverse += self.SimulateOneTrainReverse()
        return riders + reverse

weather = np.random.choice(['inclement', 'sunny'])
big_events = np.random.choice(['True', 'False'])

sim1 = TrainSimulation(stations, 200, weather , big_events)
print(sim1.SimulateOnce())
sim1.RunSimulation(10)
