#!/usr/bin/env python
import matplotlib
import sys
from subprocess import check_output

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pylab as plt

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


class NVIDIA_MEM_GUI():

    def __init__(self):

        self.root = Tk.Tk()
        self.root.wm_title("GPU MEMORY DISPLAY")
        self.root.protocol('WM_DELETE_WINDOW', self.quit_button_cb)

        fig = plt.figure(figsize=(8, 3))

        self.subplot = plt.subplot(211)
        plt.gca().invert_xaxis()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)

        self.max_gpu_mem = None
        self.current_gpu_mem = None
        self.mem_data = [0] * 100
        self.mem_range = list(reversed(range(100)))

        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        self.update()

        Tk.mainloop()

    def quit_button_cb(self, *args):

        self.root.quit()
        self.root.destroy()


    def update(self):
        self.draw()

        r = check_output(["nvidia-smi"])

        #get max gpu mem
        if self.max_gpu_mem is None:
            max_gpu_mem_index = r.rfind("MiB")
            self.max_gpu_mem = int(r[max_gpu_mem_index-6:max_gpu_mem_index].split()[0])

        #get current gpu_mem in use
        MiB_index = r.find("MiB")
        self.current_gpu_mem = int(r[MiB_index-5:MiB_index].split()[0])

        self.mem_data.pop(0)
        self.mem_data.append( 100.0 * self.current_gpu_mem / self.max_gpu_mem)

        self.show_plot()
        self.root.after(1000, self.update)

    def show_plot(self):

        self.subplot.clear()

        self.subplot.set_ylabel("Percent in use.")
        self.subplot.set_xlabel("Seconds Past")
        plt.title("GPU Memory in use of : " + str(self.current_gpu_mem) + "/" + str(self.max_gpu_mem) + "MiB; " + "{0:.2f}".format(self.mem_data[-1]) + "%")

        plt.plot(self.mem_range, self.mem_data)

    def draw(self):
        self.root.update()
        self.canvas.draw()
        self.canvas.show()


if __name__ == "__main__":
    gui = NVIDIA_MEM_GUI()