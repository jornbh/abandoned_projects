import matplotlib 
import numpy as np
matplotlib.use("TkAgg") # Man endrer backenden (?)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk 


import time
import  matplotlib.animation as animation 
from matplotlib import style 
style.use("ggplot")



import tkinter as tkinter
from tkinter import ttk #?



import random



import sys
import os
sys.path.append("GUI")
import GUI_app


import displayedTexts as TXT
import multiprocessing

from abc import ABC # Makes a class into an abstract base class

TEXT_WIDTH = 52


class base_graphPage(tk.Frame, ABC): 

    def __init_variables(self, parent, controller, figsize = 1, dpi = 50): 
        self.q = multiprocessing.Queue()
        self.f = Figure(figsize = (figsize,figsize*1.2), dpi = dpi) # Change this to make another figure size
        self.a = self.f.add_subplot(111)
        self.controller = controller

        self.inputFrame = tk.Frame(self)
        self.buttonFrame = tk.Frame(self)
        self.plotFrame = tk.Frame(self)
        self.titleFrame = tk.Frame(self)
        self.textFrame = tk.Frame(self)
        self.descriptionFrame = tk.Frame(self)

        self.parameterEntries = {}


    def __init__(self, parent, controller, figsize = 10):
        tk.Frame.__init__(self,parent)
        self.__init_variables(parent, controller, figsize)

        self.__init_frames()
        label = tk.Label(self.titleFrame, text = self.title, font = GUI_app.LARGE_FONT)
        label.pack(pady =10, padx =10)


        self.__init_plotFrame()
        self.__init_descriptionFrame()
        self.__init_text()
        self.ani = animation.FuncAnimation(self.f, self.animate, interval = 100)


        self.f.canvas.mpl_connect('pick_event', self.onClickInPlot)



    


    def __init_frames(self): 



        self.inputFrame.grid(  row =  2, column = 1 , stick = "nsew" , padx=10, pady=10)
        self.buttonFrame.grid( row =  4, column = 1 , stick = "ne" , padx=10, pady=10)
        self.plotFrame.grid(   row =  2, column = 3 , stick = "nsew" , padx=10, pady=10, columnspan =2, rowspan = 10)
        self.titleFrame.grid(  row =  0, column = 3 , stick = "nsew" , padx=10, pady=10)
        self.textFrame.grid(  row =  3, column = 1 , stick = "nsew" , padx=10, pady=10)
        self.descriptionFrame.grid(row =  5, column = 1 , stick = "nsew" , padx=10, pady=10, columnspan =2, rowspan =2)




    def __init_descriptionFrame(self): 
        #TODO ALLIGN THE TEXT LEFT
        self.descriptionLabel = tk.Text(self.descriptionFrame, height=9, width = int(TEXT_WIDTH+20), borderwidth=0)
        
        self.descriptionLabel.insert(1.0, "Description...")
        self.descriptionLabel.insert(tk.END, "?")
        self.descriptionLabel.delete(1.0, tk.END)
        self.descriptionLabel.insert(1.0, "!")

        self.descriptionLabel.configure(state="disabled")

        self.descriptionLabel.configure(bg=self.inputFrame.cget('bg'), relief=tk.FLAT)

        self.scrollbar = tk.Scrollbar(self.descriptionFrame, command=self.descriptionLabel.yview)
        
        self.descriptionLabel.configure(yscrollcommand=self.scrollbar.set)


        # self.descriptionLabel = tk.Label(self.descriptionFrame, text = "Hello", anchor = tk.W)
        self.descriptionLabel.grid(row =0, column =0, stick = "ew")
        self.scrollbar.grid(row =0, column =1, stick="wns")
    def setDescription(self, text): 

        self.descriptionLabel.configure(state="normal")
        self.descriptionLabel.delete(1.0, tk.END)
        self.descriptionLabel.insert(1.0, text)
        self.descriptionLabel.configure(state="disabled")




    def __init_plotFrame(self):
        canvas = FigureCanvasTkAgg(self.f, self.plotFrame )
        canvas.mpl_connect('pick_event', self.onClickInPlot)
        canvas.draw()

        canvas.get_tk_widget().grid( row =0, column =0, sticky = "nsew")





    def __init_text(self): 
        self.prefixes = []
        self.textEntries = {}

        self.textBox = tk.Text(self.textFrame, height=10, width = TEXT_WIDTH, borderwidth=0)

        self.textBox.insert(1.0, TXT.preSimulationMessage)

        self.textBox.configure(state="disabled")
        # self.textBox.configure(bg=self.textFrame.cget('bg'), relief=tk.FLAT)

        self.textBox.grid(row = 0, column = 0, stick = "w")

        # Make menu for copy-pasting
        self.textMenu = tk.Menu(self.textFrame, tearoff =0)
        self.textMenu.add_command(label = "Copy     (CRTL+C)", command = lambda :self.copyToClipboard( self.textBox))

        
        self.textBox.bind("<Button-3>",  lambda event: self.popup( self.textMenu, event) )

    def copyToClipboard(self, source):
        try:
            clipboardText = self.textBox.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            clipboardText = self.textBox.get(1.0, tk.END)
        self.controller.clipboard_clear()
        self.controller.clipboard_append(clipboardText)



    def popup(self, popupMenu, event):
        try:
            popupMenu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            popupMenu.grab_release()
        




    def displayTextFromResult( self, prefix, text):
        if prefix not in self.textEntries:

            self.prefixes.append(  prefix)
            
            
            
        self.textEntries[prefix] = str(text)


        # Reinsert text
        self.textBox.configure(state="normal")
        maxPrefixLen = len(max(self.prefixes, key=len))
        text = "\n".join( [ i.ljust(maxPrefixLen+3) + "\t"+self.textEntries[i] for i in self.prefixes])
        self.textBox.configure(state="normal")
        self.textBox.delete(1.0, tk.END)
        self.textBox.insert(1.0, text)
        self.textBox.configure(state="disabled")


    def startPageTask(self): # called when the start button is pressed
        self.displayTextFromResult(TXT.progressStatusLabel, TXT.progressStatusFirstRunningMessage)
        args, kwargs = self.getInputs()
        inputs = [self.q, self.workFunction,self.logger, args, kwargs]
        process = multiprocessing.Process( target = work, args = inputs )
        process.start()
        return True

    def getInputs(self):
        ...
    def plotFunction(self, result, target = None):
        ...
    def workFunction(self, *args, **kwargs):
        ... 
    def printFunction(self, printResult):
        print(printResult)            
        for i in printResult:
            self.displayTextFromResult(*i)
            
    def animate(self,i): 
        if not self.q.empty():
            printResult, plotResult = self.q.get(block = True)
            
            if printResult != None:
                self.printFunction(printResult)
            if plotResult != None:
                self. a.clear()
                processedResult = self.plotFunction( plotResult, target=( self.f, self.a))
                if processedResult != None:
                    self.printFunction(processedResult)
          
    def onClickInPlot(self, event):
        #TODO: Display coordinates of click event as a textbox INSIDE the plot
        artist = event.artist
        x, y = artist.get_xdata(), artist.get_ydata()
        ind = event.ind
        vertex_x = x[ind[0]]
        vertex_y = y[ind[0]]
        self.displayTextFromResult("X-position of clicked vertex: ", vertex_x)
        self.displayTextFromResult("Y-position of clicked vertex: ", vertex_y)
                      



# work Must be an external function (Called when the start button is pressed)
def work(objectPlot_queue, work_function, logger, args, kwargs):
    startTime = time.process_time()
    logger.cleanUp()
    progressQueue = progressQueueClass(objectPlot_queue)
    printResult, plotResult = work_function(progressQueue , *args, logger = logger, **kwargs)
    #Dump result to logger
    logger.set_plotResults(plotResult)
    logger.savePlotData(args, kwargs)
    logger.saveRawSimulationData(args,kwargs)
    objectPlot_queue.put(  ( [(TXT.progressStatusLabel, TXT.progressStatusWhenFinished)] + printResult, plotResult) )

    objectPlot_queue.put(([(TXT.logFilesLocationLabel, logger.absPath), (TXT.simulationTimeLabel, time.process_time() - startTime)], None))
    print("Done!")







class progressQueueClass:
    def __init__(self, outputQueue):
        self.q = outputQueue
    def put(self, stepNo, totalSteps):
        if self.q.empty():
            progressString = "{}% ".format( int(100*( stepNo/totalSteps)))
            self.q.put(([(TXT.progressStatusLabel, progressString)], None))




