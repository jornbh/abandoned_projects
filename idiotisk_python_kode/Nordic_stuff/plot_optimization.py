import tkinter as tk



# Own imports
import sys
sys.path.append("GUI")
sys.path.append("Simulator/Network_models")
sys.path.append("Simulator")
sys.path.append("Plot_functionality")




from base_simulatorPlotPage import base_simulatorPage
# import plot_sim_result
# from packet_statuses import PACKET_STATUS

# import bandwidth_with_drift as SIM
# from plot_sim_result import plot_list_as_hist
import numpy as np
from mpl_toolkits.axes_grid1 import Divider, LocatableAxes, Size

class OptimixationPage(base_simulatorPage):




    def __init__(self,parent, controller): 
        self.title = " Period received histogram"
        self.workFunction = workFunction
        # self.workFunction = lambda *args, **kwargs: workFunction(*args, **kwargs, outputQueue = self.q)
        self.plotFunction = lambda *x, **y : ( plotProbePoints(x[0][0], x[0][1],self.f, self.a))
        # self.plotFunction = lambda *x, **y : (print("XXXXXXX", x ))


        base_simulatorPage.__init__(self, parent, controller)



    #####################################

    def getInputs(self):
        args, kwargs = base_simulatorPage.getInputs(self)
        kwargs['outputQueue'] = self.q
        return args, kwargs


    #####################################




class putClass:
    def __init__(self, q):
        self.q =q 
    def put(self, probePoints):
        self.q.put( probePoints.transpose())




# Must be outside the class        
def workFunction(*args, **kwargs):
    ####################
    sys.path.append("Helping_funcionts")
    import nelder_mead

    q = kwargs['outputQueue']
    kwargs.pop('outputQueue')
    print(args, kwargs)
    print("Result ", SIM.bandwidthWithDrift(*args, **kwargs) == 0 )
    print( sum((sum( 0 == SIM.bandwidthWithDrift(*args, **kwargs) ))))

    f = lambda *x, **y: sum((sum( 0 == SIM.bandwidthWithDrift(*x, **y) )))
    result  = nelder_mead.maximize( f, args, [0,2], kwargs, [], integerIndexes =[0,1], integerKwargs = [], outputQueue  = putClass(q), positiveIndexes= [0,1])
    print("result", result)
    opt_val, opt_point  = result
    ####################

    returnValue = np.array([opt_point, opt_point]).transpose()  # Just so that plot function can plot the optimal point
    return returnValue


old_xLims = [0., 1.]
old_yLims = [0., 1.]

def plotProbePoints(X, Y, fig, ax): 
    global old_xLims, old_yLims

    try:
        xMin = min( old_xLims[0], min(X), 0)
        xMax = max( old_xLims[1], max(X)*1.1, 100)
        yMin = min( old_yLims[0], min(Y), 0)
        yMax = max( old_yLims[1], max(Y)*1.1, 100)
        ax.set_xlim([xMin, xMax])
        ax.set_ylim([yMin, yMax])
        old_xLims = ax.get_xlim()
        old_yLims = ax.get_ylim()

    except:
        print("PLOT FAILED ", "X=",X, "Y=", Y)

    print("old_xLims", old_xLims)
    X_new = np.append(X, [X[0]])
    Y_new = np.append(Y, [Y[0]])


    ax.plot(X_new, Y_new, "o-")
















def main():
    import GUI_app
    from plot_checkinTimePage import checkinTimePage
    app = GUI_app.MyApp()
    app.addPageToWorld( checkinTimePage, "Checkin Time" )
    app.addPageToWorld( OptimixationPage, "Optimixation Page" )

    app.mainloop()

if __name__ == '__main__':
    main()

