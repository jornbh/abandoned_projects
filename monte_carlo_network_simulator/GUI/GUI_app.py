import tkinter as tk 
import displayedTexts as TXT

LARGE_FONT = ("Verdana", 12)

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)

        self.windowHeight = 1024
        self.windowwidth = 768
        self.geometry(str(self.windowHeight)+"x"+ str(self.windowwidth))
        self.tk.call('tk', 'scaling', '-displayof', '.', 1.2)

        self.container.pack(side = "top", fill = "both", expand = True)

        self.title(TXT.simulatorTitle)

        self.container.grid_rowconfigure(0, weight =1)  # 0 er minimum størrelse, weight er en prioritets-ting
        self.container.grid_columnconfigure(0, weight =1) 

        self.frames = {}
        self.init_menu()





    def show_frame(self, cont): 
        for i,j in self.frames.items():
            j.ani.event_source.stop()
        frame = self.frames[cont]
        frame.tkraise()
        
        frame.ani.event_source.start()

    def popupMessage(self, string, title = TXT.simulatorTitle):
        popup = tk.Tk()
        def exitPopup():
            popup.destroy()
        popup.title(title)
        label = tk.ttk.Label(popup, text = string)
        label.pack()
        button = tk.ttk.Button(popup, text = "Ok", command = exitPopup)
        button.pack()
        pos_string = "+{}+{}".format(int(self.windowHeight/2), int(self.windowwidth/2))
        popup.geometry(pos_string)
        popup.mainloop()
    
    def init_menu(self): 
        menu = tk.Menu(self)
        self.config(menu= menu)
        fileMenu = tk.Menu(menu)
        menu.add_cascade(label= "File", menu = fileMenu)


        # fileMenu.add_command(label= " Display logfile-location", command=  lambda:print("Nothing is implemented"))
        # self.controller.clipboard_append("HELLO") # Copies "Hello" to the users clipboard
        fileMenu.add_command(label= TXT.aboutLabel, command=  lambda:self.popupMessage(TXT.aboutText))


        fileMenu.add_separator()
        fileMenu.add_command(label= " Exit", command=  quit)


        self.simulators = []
        self.simulatorMenu = tk.Menu(menu)
        menu.add_cascade(label = "Simulators", menu = self.simulatorMenu)



    def addPageToWorld(self, ClassName, Title, *args, **kwargs):
        self.frames[ClassName] = ClassName(self.container, self, *args, **kwargs)
        self.frames[ClassName].grid(row =0, column=0, sticky = "nsew")
        self.simulatorMenu.add_command(label = Title, command = lambda: self.show_frame(ClassName))
        self.show_frame(ClassName)





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
    print("Starting GUI")
    from plot_bandwidthAtGatewayNode import bandwidthAtGatewayNode_page
    from plot_bandwidthAtTransmittingNodes import bandwidthAtTransmttingNodes_page
    from plot_checkInTime import checkInTime_page

    app = MyApp()
    app.addPageToWorld( bandwidthAtTransmttingNodes_page, TXT.title_bandwidthAtTransmittingNode  )                 
    app.addPageToWorld( bandwidthAtGatewayNode_page,      TXT.title_bandwidthAtGatewayNode       )            
    app.addPageToWorld( checkInTime_page,                 TXT.title_checkInTime                  ) 



    app.mainloop()
