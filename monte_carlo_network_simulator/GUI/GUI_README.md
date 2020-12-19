


# Graphical User Interface 


The GUI is divided up into pages, which the user can switch between. All of them inherit from base_simulatorPage.

GUI_app functions as the "Main" for the program. For a page to be added, addPageToWorld() must be called, and given the class of the page that is to be added, as well as a string containing its name.

## GUI architecture
![Alt text](GUI_architecture.png?raw=true "Title")


## Required functionality from new child-pages

All pages that inherit from the base_simulatorPage (a viritual class) has to implement workFunction() and plotFunction(). 

workFunction() takes in the arguments and keyword-arguments returned from getInputs().
* The arguments defaults to progressQueue, pluss  the arguments   needed to run a single simulation). 
* The keyword-arguments default to a logger-object, which takes in the raw simulationData, as well as the default keyword-argments provided by the user, that are used in the simulation. 
*


### Optional functionality from child-classes
* For more input-parameters, the getInputs()- function can be overloaded to give more return-values ( Returns a list and a dictionary). 
* addParameter() can be called with a string and a default value to display one more input that the user can give in 
* The text-fields the user writes into can be accesed directly by calling _getInput() with the same string used to label the parameter

