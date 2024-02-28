import logging
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import time
from constants import LoggerNames
from utilities import setup_logger

# logger = logging.getLogger(LoggerNames.GUI)
formatter = logging.Formatter('{asctime} - {name:10s} - {levelname:8s} - {message}', '%Y%m%d-%H:%M:%S', style='{')
logger = logging.getLogger(LoggerNames.GUI)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

status = "Not Running"

def check_meshnet():
    return True

def start_meshnet():
    global status
    print("Starting")
    logger.info("Starting Meshnet via GUI")
    # subprocess.run(["pkexec", "systemctl", "start", "meshnet.service"])
    start = time.time()
    timeout = 3
    while not check_meshnet() and time.time() < start + timeout:
        time.sleep(1)
    if check_meshnet():
        messagebox.showinfo("Info", "Meshnet Started") 
        status = 'Running'
        status_meshnet()
    else:
        messagebox.showwarning('Warning', "Unable to start meshnet")
        status = 'Not Running'
        status_meshnet()

def stop_meshnet():
    global status
    print("Stopping")
    # logger.info("Stopping Meshnet via GUI")
    # subprocess.run(["pkexec", "systemctl", "stop", "meshnet.service"])
    start = time.time()
    timeout = 3
    while check_meshnet() and time.time() < start + timeout:
        time.sleep(1)
    if not check_meshnet():
        messagebox.showinfo("Info", "Meshnet Stopped") 
        status = 'Not Running'
        status_meshnet()
    else:
        messagebox.showwarning('Warning', "Unable to stop meshnet")
        status = 'Running'
        status_meshnet()

def update_config():
    print("Updating config file")
    # logger.info("Stopping Meshnet via GUI")
    # subprocess.run(["pkexec", "systemctl", "stop", "meshnet.service"])

def write_xbee():
    print("Writing to xbee")
    # logger.info("Stopping Meshnet via GUI")
    # subprocess.run(["pkexec", "systemctl", "stop", "meshnet.service"])

def status_meshnet():
    global status
    print("Status meshnet")
    # logger.info("Stopping Meshnet via GUI")
    # subprocess.run(["pkexec", "systemctl", "stop", "meshnet.service"])
    status_label2['text'] = status

window = tk.Tk(className="meshnet")
window.wm_title("MeshNet Controller")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

n = ttk.Notebook(window)
n.grid(sticky='nsew')
n.rowconfigure(0, weight=1)
n.columnconfigure(0, weight=1)

# Run page
f1 = ttk.Frame(n)
f1.grid(sticky='nsew')
n.add(f1, text='Run')
f1.rowconfigure(0, weight=1)
f1.columnconfigure([0,1,2], weight=1)

btn_frame = tk.Frame(f1)
btn_frame.grid(row=0, column=1)
status_frm = tk.Frame(btn_frame)
status_frm.grid(row=0)
status_label = tk.Label(status_frm, text="Status:")
status_label.grid(row=0, column=0)
status_label2 = tk.Label(status_frm, text=status, background='white', width=15)
status_label2.grid(row=0, column=1)
status_btn = tk.Button(btn_frame, text="Status Meshnet", command=status_meshnet, height=2, width=20)
status_btn.grid(row=1)
start_btn = tk.Button(btn_frame, text="Start Meshnet", command=start_meshnet, height=2, width=20)
start_btn.grid(row=2)
stop_btn = tk.Button(btn_frame, text="Stop Meshnet", command=stop_meshnet, height=2, width=20)
stop_btn.grid(row=3)

# Config page
input_width = 20
row_num = 0
f2 = ttk.Frame(n, padding=75)
f2.grid(sticky='nsew')
n.add(f2, text='Configure')

ip_desc = tk.Label(f2, text="IP: Choose a unique IPv4 IP address for this XBee node", anchor='w')
ip_desc.grid(row=row_num, column=0, columnspan=2, sticky='we')
row_num += 1
port_desc = tk.Label(f2, text="Port: Enter the USB port device for the XBee", anchor='w')
port_desc.grid(row=row_num, column=0, columnspan=2, sticky='we')
row_num += 1
baud_desc = tk.Label(f2, text="Baud: Choose a baud rate from the following:", anchor='w')
baud_desc.grid(row=row_num, column=0, columnspan=2, sticky='we')
row_num += 1
baud_desc2 = tk.Label(f2, text="      1200, 2400, 4800, 9600, 19200,", anchor='w')
baud_desc2.grid(row=row_num, column=0, columnspan=2, sticky='we')
row_num += 1
baud_desc3 = tk.Label(f2, text="      38400, 57600, 115200, 230400", anchor='w')
baud_desc3.grid(row=row_num, column=0, columnspan=2, sticky='we')
row_num += 1
net_id_desc = tk.Label(f2, text="Net ID: choose a whole number from 0 to 32767", anchor='w')
net_id_desc.grid(row=row_num, column=0, columnspan=2, sticky='we')
row_num += 1
net_id_desc = tk.Label(f2, text="Subnet: Set the subnet mask", anchor='w')
net_id_desc.grid(row=row_num, column=0, columnspan=2, sticky='we')
row_num += 1

ip_label = tk.Label(f2, text="IP:", anchor='w')
ip_label.grid(row=row_num, column=0)
ip_entry = tk.Entry(f2, width=input_width)
ip_entry.grid(row=row_num, column=1)
row_num += 1
ip_entry.insert(0, "10.0.0.1")

port_label = tk.Label(f2, text="Port:", anchor='w')
port_label.grid(row=row_num, column=0)
port_entry = tk.Entry(f2, width=input_width)
port_entry.grid(row=row_num, column=1)
row_num += 1
port_entry.insert(0, "/dev/ttyUSB0")

baud_label = tk.Label(f2, text="Baud:", anchor='w')
baud_label.grid(row=row_num, column=0)
baud_entry = tk.Entry(f2, width=input_width)
baud_entry.grid(row=row_num, column=1)
row_num +=1
baud_entry.insert(0, "230400")

net_id_label = tk.Label(f2, text="Net ID:", anchor='w')
net_id_label.grid(row=row_num, column=0)
net_id_entry = tk.Entry(f2, width=input_width)
net_id_entry.grid(row=row_num, column=1)
row_num +=1
net_id_entry.insert(0, "5000")

subnet_label = tk.Label(f2, text="Subnet:", anchor='w')
subnet_label.grid(row=row_num, column=0)
subnet_entry = tk.Entry(f2, width=input_width)
subnet_entry.grid(row=row_num, column=1)
row_num +=1
subnet_entry.insert(0, "255.255.255.0")

save_btn = tk.Button(master=f2, text="Update config file", command=update_config, height=2, width=20)
save_btn.grid(row=row_num, column=0, columnspan=2, pady=20)
row_num += 1

write_btn = tk.Button(master=f2, text="Write to Xbee", command=write_xbee, height=2, width=20)
write_btn.grid(row=row_num, column=0, columnspan=2)
row_num += 1

window.mainloop()