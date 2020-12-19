import tkinter as tk 

LARGE_FONT = ("Verdana", 12)

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)


        self.container.pack(side = "top", fill = "both", expand = True)


        self.container.grid_rowconfigure(0, weight =1)  # 0 er minimum størrelse, wait er en prioritets-ting
        self.container.grid_columnconfigure(0, weight =1) 

        self.frames = {}
        self.init_menu()





    def show_frame(self, cont): 
        frame = self.frames[cont]
        frame.tkraise()
    
    def init_menu(self): 
        menu = tk.Menu(self)
        self.config(menu= menu)
        fileMenu = tk.Menu(menu)
        menu.add_cascade(label= "File", menu = fileMenu)


        fileMenu.add_command(label= " Save...", command=  lambda:print("Nothing is implemented"))
        fileMenu.add_command(label= " Load....", command=  lambda:print("Nothing is implemented"))
        fileMenu.add_separator()
        fileMenu.add_command(label= " Nothing is implemented....", command=  lambda:print("Nothing is implemented"))


        self.simulators = []
        self.simulatorMenu = tk.Menu(menu)
        menu.add_cascade(label = "Simulators", menu = self.simulatorMenu)



    def addPageToWorld(self, ClassName, Title, *args, **kwargs):
        self.frames[ClassName] = ClassName(self.container, self, *args, **kwargs)
        self.frames[ClassName].grid(row =0, column=0, sticky = "nsew")
        self.simulatorMenu.add_command(label = Title, command = lambda: self.show_frame(ClassName))





# Can also append new pages during run-time
class StartPage(tk.Frame): 
    def __init__(self,parent, controller, title = "Start Page"):
        self.title= title
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = title, font = LARGE_FONT)
        label.pack(pady =10, padx =10)
        self.parent = parent
        self.buttons = []
        self.controller = controller
        for b in self.buttons:
            b.pack()
    
    def appendPage(self, ClassName, Title, *args, **kwargs): 
        
        self.buttons.append(tk.Button(self, text = Title, command = lambda : self.controller.show_frame(ClassName) ))
        self.buttons[-1].pack()




def main(): 
    # from plot_checkinTimePage import checkinTimePage
    from plot_optimizationPage import OptimixationPage
    # from plot_averageBandwidths import averageBandwidthPage
    # from plot_totalBandwidthOverNumberOfNodes import totalBandwidthOverNumberOfNodes_page
    # from plot_averageBandwidthOverNumberOfNodes import averageBandwidthOverNumberOfNodes_page
    app = MyApp()
    # app.addPageToWorld( checkinTimePage, "Checkin Time" )
    # app.addPageToWorld( averageBandwidthPage, "AverageBandwidth Page" )
    # app.addPageToWorld( totalBandwidthOverNumberOfNodes_page, "Total Bandwidth Over Number Of Nodes Page" )
    # app.addPageToWorld( averageBandwidthOverNumberOfNodes_page, "Average Bandwidth Over Number Of Nodes Page" )
    app.addPageToWorld( OptimixationPage, "Optimixation Page" )



    app.mainloop()


if __name__=="__main__":
    main()