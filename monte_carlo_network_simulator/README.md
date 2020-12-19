# Simple BLE Simulator
This is a simple network simulator intended for probing interference when you have multiple advertisers.
The simulator only supports advertisement on a single channel and it only supports one configuration: A circle network where the receiver/gateway are equidistant to the n transittors.


## Accuracy of the simulator
We have conducted some physical test and verified that the simulator is accurate for simulations with little traffic. Our test setup with 7 transmittors deviated from the Simulator when they where asynchroneous with a Transmission Period = Jitter = 7 ms. I.e. For asynchroneus settings the Transmission Period [ms] should be greater than nNodes to ensure accuracy. You will need at least 200 Simulations to get a representative result.

## Different environments
### Windows 10
Tested and working
### Windows 7
Tested and working
### OSX
Tested and currently not working
### Linux
Not tested



# User-guide





# System architecture

[GUI-architecture](GUI/GUI_README.md)

[SIMULATOR-architecture](Simulator/Simulator_README.md)







