# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

import numpy as np

import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)
global var
var=0
n = 1000
t = np.linspace(0, 8, n)
T = t[1] - t[0]
global x1,fig,f1,fg,sfreq,fmul,fgmul,fig2,f2
global x2
global v
global v1
global f
global sfreq


a0 = 5
f0 = 1
delta_f = 1.0


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Convoloution")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="click and start your convoloution",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()
class PageOne(tk.Frame):
    x1= np.sin(t)
    x2 = np.cos(t)

    def __init__(self, parent, controller):
        global v1
        global v
        global sfreq
        global samp

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="choose your Convoloution here", font=LARGE_FONT)
        label.pack(pady=10, padx=10)



        v = tk.IntVar()
        v1 = tk.IntVar()
        label = tk.Label(self, text="select your first function",justify = tk.LEFT)
        label.pack(pady=10, padx=100)



        tk.Radiobutton(self,
                       text="Sin(t)",
                       padx=20,
                       variable=v,
                       value=1, command=self.sel).pack(anchor=tk.W)
        tk.Radiobutton(self,
                       text="Cos(t)",
                       padx=20,
                       variable=v,
                       value=2, command=self.sel).pack(anchor=tk.W)
        tk.Radiobutton(self,
                       text="pulse(t)",
                       padx=20,
                       variable=v,
                       value=3, command=self.sel).pack(anchor=tk.W)
        tk.Radiobutton(self,
                       text="Sinc(t)",
                       padx=20,
                       variable=v,
                       value=4, command=self.sel).pack(anchor=tk.W)
        label = tk.Label(self, text="select your second function", justify=tk.LEFT)
        label.pack(pady=10, padx=100)

        tk.Radiobutton(self,
                       text="Sin(t)",
                       padx=20,
                       variable=v1,
                       value=1, command=self.sel1).pack(anchor=tk.W)
        tk.Radiobutton(self,
                       text="Cos(t)",
                       padx=20,
                       variable=v1,
                       value=2, command=self.sel1).pack(anchor=tk.W)
        tk.Radiobutton(self,
                       text="pulse(t)",
                       padx=20,
                       variable=v1,
                       value=3, command=self.sel1).pack(anchor=tk.W)
        tk.Radiobutton(self,
                       text="Sinc(t)",
                       padx=20,
                       variable=v1,
                       value=4, command=self.sel1).pack(anchor=tk.W)
        button3 = ttk.Button(self, text="See your convoloution"
                          ,command=self.myfunc
                             )

        button3.pack()

        axcolor = 'lightgoldenrodyellow'
        axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        #axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

        sfreq = Slider(axfreq, 'Change', 0.1, 30.0, valinit=f0, valstep=delta_f)
        #samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)
        sfreq.on_changed(self.update1)
        #samp.on_changed(self.update1)




    def sel(self):


        global x1

        if v.get() == 1:

            x1 = np.sin(t);


        elif v.get() == 2:

            x1 = np.cos(t);
        elif v.get() == 3:

            x1 = np.where(t <= 4, 1, 0)  # build input functions
        elif v.get() == 4:

            x1 = np.sinc(t);
        else:

            print("nothing found 1")

    def sel1(self):
        global x2

        if v1.get() == 1:

            x2 = np.sin(t);

        elif v1.get() == 2:

            x2 = np.cos(t);
        elif v1.get() == 3:

            x2 = np.where(t <= 4, 1, 0)  # build input functions
        elif v1.get() == 4:
            x2 = np.sinc(t);
        else:
            print("nothing found 2")

    def update1(val,self):
        global x1,sfreq,f,fig,f1,fg,fmul,fgmul
        freq = sfreq.val

        if v.get() == 1:

            x1 = np.sin(t+freq);

        elif v.get() == 2:

            x1 = np.cos(t+freq);
        elif v.get() == 3:

            x1 = np.where(t <= 4-freq, 1, 0)  # build input functions
        elif v.get() == 4:

            x1 = np.sinc(t+freq);
        else:
            print ("nothing found update")

        f.set_ydata(x1)


        y1 = np.convolve(x1, x2, mode='full') * T
        f1.set_ydata(y1)

        ymul2=np.multiply(x1,x2)
        fmul.set_ydata(ymul2)

        fgmul.canvas.draw_idle()
        fig.canvas.draw_idle()
        fg.canvas.draw_idle()



    def myfunc(x):
        global f,fig,f1,fg,var,fmul,fgmul,fig2,f2

        if var==0:

            var=1
            y = np.convolve(x1, x2, mode='full') * T  # scaled convolution

            ty = np.linspace(0, 2 * 8, n * 2 - 1)  # double time interval
            fig = plt.figure(1)

            ax1 = fig.add_subplot(211)
            f, =ax1.plot(t+f0, x1,label="x_1")

            fig2,ax2=plt.subplots(1,1)
            f2, =ax2.plot(t, x2, label="x_2",color='yellow')
            ax2.legend(loc='best')


        # plot results:
            ymul=np.multiply(x1,x2)
            fgmul , axmul=plt.subplots(1,1)
            fmul, =axmul.plot(t, ymul, label="$x_1\\dot x_2$",color='green')
            axmul.legend(loc='best')

            fg, ax = plt.subplots(1, 1)
            f1, =ax.plot(ty, y, label="$x_1\\star x_2$",color='red')
            ax.legend(loc='best')
            ax.grid(True)

            plt.show()
        else :
            sfreq.reset()
            f.set_ydata(x1)
            f2.set_ydata(x2)
            y2 = np.convolve(x1, x2, mode='full') * T
            ymul2=np.multiply(x1,x2)

            f1.set_ydata(y2)
            fmul.set_ydata(ymul2)

            fig.canvas.draw_idle()
            fig2.canvas.draw_idle()
            fgmul.canvas.draw_idle()
            fg.canvas.draw_idle()

app = SeaofBTCapp()

app.mainloop()
