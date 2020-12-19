# Star topology simulator


The simulator is made up of three parts to become a complete model. 
* Network-model
    * Better name might be network-behaviour
* Transmission-model
* Signal-strength-model
    * Better name is interference-model

The network-model describes the behaviour of the network (All to one star-topology). The network-model needs to take in the other two models as keyword-arguments, but will default to assuming all nodes to have the same signal-strength.

![Alt text](Simulator-architecture.png?raw=true "Title")

![Alt text](Simulator-information-flow.png?raw=true "Title")
