import matplotlib 
import numpy as np
matplotlib.use("TkAgg") # Man endrer backenden (?)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk 



import  matplotlib.animation as animation 
from matplotlib import style 
style.use("ggplot")



import tkinter as tkinter
from tkinter import ttk #?



import random



import sys 
sys.path.append("GUI")
import GUI_app



import multiprocessing

from abc import ABC # Makes a class into an abstract base class


class base_graphPage(tk.Frame, ABC): 

    def __init_variables(self, parent, controller): 
        self.q = multiprocessing.Queue()
        self.f = Figure(figsize = (5,5), dpi = 100) 
        self.a = self.f.add_subplot(111)


        self.inputFrame = tk.Frame(self)
        self.buttonFrame = tk.Frame(self)
        self.plotFrame = tk.Frame(self)
        self.titleFrame = tk.Frame(self)

        self.entries = []
        self.buttons =[]

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.__init_variables(parent, controller)
     
        self.__init_frames()
        label = tk.Label(self.titleFrame, text = self.title, font = GUI_app.LARGE_FONT)
        label.pack(pady =10, padx =10)


        self.__init_plotFrame()
        self.ani = animation.FuncAnimation(self.f, self.animate, interval = 10)





    def __init_frames(self): 



        self.inputFrame.grid(  row =  2, column = 1 , stick = "nsew" , padx=10, pady=10)
        self.buttonFrame.grid( row =  2, column = 0 , stick = "nsew" , padx=10, pady=10)
        self.plotFrame.grid(   row =  2, column = 3 , stick = "nsew" , padx=10, pady=10)
        self.titleFrame.grid(  row =  0, column = 3 , stick = "nsew" , padx=10, pady=10)




    def __init_plotFrame(self):
        canvas = FigureCanvasTkAgg(self.f, self.plotFrame)
        canvas.show()
        canvas.get_tk_widget().pack( side = tk.TOP, fill = tk.BOTH, expand = True)


        toolbar = NavigationToolbar2TkAgg(canvas, self.plotFrame)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

    def startPageTask(self): 

        args, kwargs = self.getInputs()
        if args==None  and kwargs == None:
            print("Invalid input")
            return False
        inputs = [self.q, self.workFunction, args, kwargs]
        process = multiprocessing.Process( target = work, args = inputs )
        process.start()
        return True

    def getInputs(self):
        ...


    def animate(self,i): 
        if not self.q.empty():
            result = self.q.get()
            
            self. a.clear()
            self.plotFunction( result, target=( self.f, self.a))





# work Must be an external function (Called when the start button is pressed)
def work(object_queue, work_function, args, kwargs):
    result = work_function(*args, **kwargs)
    object_queue.put(  result )




