from customtkinter  import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter.messagebox
import EulerMaruyamaAlg as c
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(CTk):
    def __init__(self):
        super().__init__()


        # window config
        self.title("SDJ uz Eulerovu metodu")
        self.geometry(f"{1100}x{580}")

        # grid
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
       

        # figure 
        self.plot_frame = CTkFrame(self)
        self.fig = Figure(figsize=(5, 5), dpi=120)
        self.ax = (self.fig).add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)  

        self.plot_frame.grid(row=0, column=1, padx=(10, 0), pady=(10, 0),columnspan = 1,rowspan = 2 ,sticky="nsew")
        
        
        # SIDEBAR
        self.sidebar_frame = CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.text = CTkLabel(self.sidebar_frame, text="Izaberi slučajan proces",\
             font=CTkFont(size=20, weight="bold"))
        self.text.grid(row=0, column=0, padx=20, pady=(20, 10))
        ##izbor SDJ
        self.radioVar = tkinter.IntVar(value=0)
        self.changeSDJ()
        self.GBG = CTkRadioButton(master=self.sidebar_frame, variable=self.radioVar, value=0\
                                             ,text = "Geometrijsko Brownovo gibanje", command=self.changeSDJ)
        self.GBG.grid(row=1, column=0, pady=10, padx=20, sticky="n")
        self.OU = CTkRadioButton(master=self.sidebar_frame, variable=self.radioVar, value=1\
                                             ,text = "Ornstein–Uhlenbeck proces", command=self.changeSDJ)
        self.OU.grid(row=2, column=0, pady=10, sticky="n")

        ## Light/Dark mode
        self.appearance_mode_label = CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
 
        # create title entry and button
        self.entry = CTkEntry(self, placeholder_text="Title of the plot")
        self.entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

    
        self.clearButton = CTkButton(master=self, fg_color="transparent",\
                                        border_width=2, text_color=("gray10", "#DCE4EE"),\
                                        text = "CLEAR PLOT",command = self.clear)
        self.clearButton.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="n")

        self.plotButton = CTkButton(master=self, fg_color="transparent",\
                                    border_width=2, text_color=("gray10", "#DCE4EE"),\
                                    text = "PLOT", command=self.plot_trajectory)
        self.plotButton.grid(row=3, column=3,  padx=(20, 20), pady=(20, 20), sticky="nsew")

        
       

   
        # Parametri simulacije
        self.simParameter = CTkFrame(self)
        self.simParameter.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="n")

        self.simParameterLabel = CTkLabel(master=self.simParameter, text="Parametri simulacije:")
        self.simParameterLabel.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="nsew")
        
        self.simParameter1 = CTkEntry(master=self.simParameter, placeholder_text="N")
        self.simParameter1.grid(row=1, column=0, columnspan=1, padx=(10, 10), pady=(20, 20), sticky="s")
        self.simParameter2 = CTkEntry(master=self.simParameter, placeholder_text="T")
        self.simParameter2.grid(row=2, column=0, columnspan=1, padx=(10, 10), pady=(20, 20), sticky="e")
        self.simParameter3 = CTkEntry(master=self.simParameter, placeholder_text="dt (default T/N)")
        self.simParameter3.grid(row=3, column=0, columnspan=1, padx=(10, 10), pady=(20, 20), sticky="n")
       


    def changeSDJ(self):
        self.sdjParameter = CTkFrame(self)
        self.sdjParameter.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.sdjParameter.grid_columnconfigure(0, weight=0)
        self.sdjParameter.grid_rowconfigure(4, weight=1)

        placeholdersParam = ["\u03bc","\u03c3","\u03b8_1","\u03b8_2","\u03b8_3"]

        self.sdjParameter = CTkLabel(master=self.sdjParameter, text="Parametri SDJ:")
        self.sdjParameter.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="nsew")

        self.labelErr = CTkLabel(self.sdjParameter, text='', fg_color="transparent")    
        self.labelErr.grid(row=3, column=0, columnspan=8 ,rowspan = 1, padx=10, pady=10, sticky="nsew")

        if self.radioVar.get() == 1:
            l1 = placeholdersParam[2]
            l2 = placeholdersParam[3]
            l3 = placeholdersParam[4]

            self.paramProcess3 = CTkEntry(master=self.sdjParameter, placeholder_text=l3)
            self.paramProcess3.grid(row=1, column=4, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        
        else:

            l1 = placeholdersParam[0]
            l2 = placeholdersParam[1]

            self.var1 = IntVar()
            self.var2 = IntVar()
            
            self.checkbox_1 = CTkCheckBox(master=self.sdjParameter,text="Dodaj egzaktan prikaz",variable=self.var1, height=10,checkbox_height=20,checkbox_width=20)
            self.checkbox_1.grid(row=0, column=12, pady=(20, 0), padx=20, sticky="ew")
            self.checkbox_2 = CTkCheckBox(master=self.sdjParameter,text="Izračunaj apsolutnu pogrešku",variable=self.var2, height=10,checkbox_height=20,checkbox_width=20)
            self.checkbox_2.grid(row=1, column=12, pady=(20, 0), padx=20, sticky="ew")
            
        

        self.paramProcess1 = CTkEntry(master=self.sdjParameter, placeholder_text=l1)
        self.paramProcess1.grid(row=1, column=0, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.paramProcess2 = CTkEntry(master=self.sdjParameter, placeholder_text=l2)
        self.paramProcess2.grid(row=1, column=2, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.paramProcessXou = CTkEntry(master=self.sdjParameter, placeholder_text="X0")
        self.paramProcessXou.grid(row=0, column=2, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")



        
    def plot_trajectory(self):
        # Čitanje parametara iz korisničkog unosa
        try:
            if self.radioVar.get() == 0:
                sdj,theta = "GBG",0 
            else:
                sdj = "OU"
                theta = float(self.paramProcess3.get())
            
            X0 = float(self.paramProcessXou.get())
            param1 = float(self.paramProcess1.get())
            param2 = float(self.paramProcess2.get())

            N = int(self.simParameter1.get())
            T = float(self.simParameter2.get())

            dt = T/N if self.simParameter3.get() == '' else float(self.simParameter3.get())

            t = np.linspace(0, 1, N)  

            model = c.SDJ(X0,param1,param2,theta,sdj)
            dB = c.BG(dt,N)
            XEm = model.EM(N,dt,dB)
            
            self.ax.plot(t,XEm)
            
            XEx = model.Exact(t,dB)
   
            if self.var1.get()==1:
                self.ax.plot(t,XEx)

            labelTxT=''

            if self.var2.get()==1:
                err = np.sum(abs(XEx-XEm))/N

                labelTxT ="Apsolutna pogreška iznosi:      " + str(err)
            
            
            self.labelErr.configure(text = labelTxT)

            title = self.entry.get() 
            if str(title != ''):
                self.ax.set_title(title)
           
            self.canvas.draw()


        except ValueError:
            tk.messagebox.showwarning(title=None, message="Nepravilno unešeni parametri")


    def change_appearance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)
        if self.radioVar.get() == 0 : self.radioVar.set(0)
        else: self.radioVar.set(1)
        self.changeSDJ()

    def clear(self):
        self.ax.clear()
        self.canvas.draw()
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()





