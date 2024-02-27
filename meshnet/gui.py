import logging
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
from constants import LoggerNames

logger = logging.getLogger(LoggerNames.GUI)

# Set up the window
window = tk.Tk(className="meshnet")
window.wm_title("MeshNet Controller")
window.rowconfigure([0, 1, 2], minsize=100, weight=1)
window.columnconfigure(0, minsize=400, weight=1)

def start_meshnet():
    logger.info("Starting Meshnet via GUI")
    subprocess.run(["pkexec", "systemctl", "start", "meshnet.service"])

def stop_meshnet():
    logger.info("Stopping Meshnet via GUI")
    subprocess.run(["pkexec", "systemctl", "stop", "meshnet.service"])

def configure():
    logger.info("Configuring Meshnet via GUI")

start_btn = tk.Button(master=window, text="Start Meshnet", command=start_meshnet, height=2, width=20)
start_btn.grid(row=0, column=0)

btn2 = tk.Button(master=window, text="Stop Meshnet", command=stop_meshnet, height=2, width=20)
btn2.grid(row=1, column=0)

btn3 = tk.Button(master=window, text="Configure", command=stop_meshnet, height=2, width=20)
btn3.grid(row=2, column=0)

window.mainloop()