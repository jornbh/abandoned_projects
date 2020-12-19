import numpy as np
from operator import itemgetter
from queue import PriorityQueue
import collections

# The API function is Maximize() further bellow


class EmptyVoid:
    def put(*args, **kwargs):
        pass


class terminationChecker:
    def __init__(self):
        self.oldPoint =None
        self.tolerance = 0.01 # Threshold for distance traveled to keep simulation going
    def check(self,new_val,new_point):
        if self.oldPoint is None: 
            self.oldPoint = new_point        
            return False
        step = new_point-self.oldPoint
        distance_squared = sum ( step*step) 
        self.oldPoint = new_point
        return distance_squared < self.tolerance



# API function
def maximize( original_function, parameters, variable_indexes, kwargs_dict, variable_kwargs_list, 
                start_points =None, 
                Print_status = False, 
                Max_itterations = 300, 
                integerIndexes = [], 
                integerKwargs = [], 
                positiveIndexes = [],
                outputQueue = EmptyVoid() ):

    integerPositions =    findIntegerPositions(  variable_indexes,              variable_kwargs_list, integerIndexes, integerKwargs)
    fun = makeFun(original_function, parameters, variable_indexes, kwargs_dict, variable_kwargs_list, integerIndexes, integerKwargs, positiveIndexes)
    if start_points == None: 
        start_points = make_startPoints(parameters, variable_indexes, kwargs_dict, variable_kwargs_list)

    f_vals = np.array([fun( i) for i in start_points])
    indexes = np.argsort(f_vals)
    f_vals = f_vals[indexes]
    print("start_points",start_points)
    print("f_vals",f_vals)
    print("indexes",indexes)


    probePoints = start_points[indexes]

    OPT_val, OPT_point = maximizationLoop(f_vals, probePoints, fun, outputQueue= outputQueue)

    return OPT_val, OPT_point





def maximizationLoop(f_vals, probePoints, fun, maxItterations = 100000000, outputQueue= EmptyVoid, is_done = terminationChecker()):
    for i in range(maxItterations):
        print(f_vals, probePoints)
        averagePoint = sum(probePoints)/ len(probePoints)
        better_val ,betterPoint = try_different_points(probePoints[0], f_vals[0],   averagePoint, probePoints[-1], f_vals[-1], fun )
        print(better_val)

        insert_improvedValue( betterPoint, better_val, probePoints, f_vals)

        if is_done.check(better_val, betterPoint): 
            print("DONE")
            print(i)
            break
        outputQueue.put(probePoints)





    return f_vals[-1], probePoints[-1]











def makeFun( o_fun, parameters, variable_indexes, kwargs_dict, variable_kwargs_list, integerIndexes,integerKwargs, positiveIndexes ): 
    used_parameters = list(parameters)
    def fun( Variables):
        for ind, elem in enumerate(variable_indexes): 
            used_parameters[elem] = Variables[ind]
        ind +=1
        for i, elem in enumerate(variable_kwargs_list): 
            kwargs_dict[elem] = Variables[ i + ind]

        for i in integerIndexes: 
            used_parameters[i] = int(used_parameters[i])
        for i in integerKwargs:
            kwargs_dict[i] = int(kwargs_dict[i])

        for i in positiveIndexes:
            used_parameters[i] = max(0, used_parameters[i])
        return o_fun(*used_parameters, **kwargs_dict)

    return fun



def findIntegerPositions(variable_indexes, variable_kwargs_list, integerIndexes, integerKwargs):
    # Returns a list that tells which elements 
    #  that are integers in the vector that we try to optimize
    integerPositions = []

    for pos, index in enumerate(variable_indexes): 
        if index in integerIndexes:
            integerPositions.append(pos)

    ofset = pos+1


    for pos, arg in enumerate(variable_kwargs_list): 
        if arg in integerKwargs:
            integerPositions.append(ofset + pos)

    return integerPositions




def get_startPointFromUser(parameters, variable_indexes, kwargs_dict, variable_kwargs_list):
    Pos = [ parameters[i] for i in variable_indexes]
    L = [ kwargs_dict[i] for i in variable_kwargs_list]
    out = np.append(Pos, np.array(L) )

    return out 



def make_startPoints(parameters, variable_indexes, kwargs_dict, variable_kwargs_list):

    userStartPoint = get_startPointFromUser(parameters, variable_indexes, kwargs_dict, variable_kwargs_list)
    basicStartPoint   = np.full( len(userStartPoint), 1 ) # Almost 0, but not quite
    extreme_point = np.array(userStartPoint)
    extreme_point*=2

    start_point_bases = [  [] ]

    for i,j in zip(extreme_point,basicStartPoint ): 
        new_bases = (   [ [float(i)] + base  for base in start_point_bases] +
                        [ [j] + base for base in start_point_bases] )
        start_point_bases = new_bases
    returnValue = np.array(start_point_bases)

    return returnValue



def try_different_points( Worst_point, Worst_val, Average, Best_point, Best_val,  function): 
    p =  Average-Worst_point
    current_point  =  Average+ p
    current_val = function( current_point )
    Average_function = function( Average)
    if current_val >= Worst_val: 
        if current_val >= Average_function:
            Even_better_point = current_point+ p #One extra step in the improving direction

            Even_better_val = function(Even_better_point)
            if Even_better_val >= current_val:
                return  Even_better_val, Even_better_point
        return current_val,current_point



    outsideContraction_point = current_point+ p/2
    outsideContraction_val = function(outsideContraction_point)
    if outsideContraction_val >= Worst_val: 
        return outsideContraction_val, outsideContraction_point

    insideContraction_point = Worst_point + p/2
    insideContraction_val = function(insideContraction_point)

    if insideContraction_val >= Worst_val:
        return insideContraction_val, insideContraction_point


    shrinking_point =(Worst_point+ Best_point)/2
    shrinking_val = function(shrinking_point)
    return shrinking_val , shrinking_point




def insert_improvedValue( betterPoint, better_fval, probePoints, f_vals): 
    index = np.searchsorted( f_vals, better_fval)


    if index == 0: # The "improved point is not actually better"
        probePoints[0] = betterPoint
        f_vals[0] = better_fval
        return 



    indexes = np.arange(index-1)
    incremented_indexes = indexes +1

    probePoints[indexes] = probePoints[incremented_indexes]


    f_vals[indexes] = f_vals[incremented_indexes]


    # Because everything has "Shifted" one place to the left, the element is placed with one index lower
    probePoints[index-1] = betterPoint
    f_vals[index-1]      = better_fval



if __name__ == "__main__":

    to_max = lambda x, y, z: -x*x -x -y*y -z*z
    print(to_max(10, 20,30))

    maximize(to_max, [0,0,0], [0,1,2], {}, [],  Print_status=True)