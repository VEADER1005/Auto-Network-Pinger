import os
import pandas as pd
import sys
import time
from threading import Thread
from queue import Queue as qu
from threading import Timer

import tkinter as tk
from tkinter import messagebox


def start():
    for file_name in file_list:
        unrechable = []
        rechable = []
        if(not qu_main.empty()):
            if(qu_main.get() == 'q'):
                qu_main.put('q')
                return
        print("Processing:"+file_name, end="\n")
        open_file(file_name, rechable, unrechable)
        if len(unrechable) > 0:
            print("These IP from " + file_name + " are Unrechable:")
            for i in unrechable:
                print(i, end="\n")
            print("")
        else:
            print("All IP's are Rechable from " + file_name)
    return


def open_file(file_name, rechable, unrechable):
    df = pd.read_excel("D:/Network/"+file_name+".xlsx")
    col_IP = df.loc[:, "IP"].tolist()
    col_name = df.loc[:, "Location"].tolist()
    check(col_IP, col_name, rechable, unrechable)
    return


def check(col_IP, col_name, rechable, unrechable):
    for ip in range(len(col_IP)):
        response = os.popen(f"ping {col_IP[ip]} ").read()
        if("Request timed out." or "unreachable") in response:
            unrechable.append(str(col_IP[ip] + " at " + col_name[ip]))
        else:
            rechable.append(str(col_IP[ip] + " at " + col_name[ip]))
    return


def main1():
    while(True):
        x = 0
        print("Script has started Execution")
        start()
        while(x < 20):
            if(not qu_main.empty()):
                if(qu_main.get() == 'q'):
                    print("The Program will now QUIT")
                    return
                else:
                    print("sleep")
                    x += 1
                    time.sleep(1)
            else:
                print("sleep")
                x += 1
                time.sleep(1)


def wait_th2():
    global th1_done
    if(not th2.is_alive()):
        print("The Program is ready to be shut Down")
        th1_done = True
    else:
        th1 = Timer(5, wait_th2)
        th1.start()


def redirect_print(output):
    text_output.insert(tk.END, output)
    text_output.see(tk.END)


def start_process():
    global th2, th1
    th1 = Timer(5, wait_th2)
    th2 = Thread(target=main1)
    th2.start()
    global th1_done, th1_progress
    th1_done = False
    th1_progress = False
    return


def on_cancel():
    global th1_progress
    qu_main.put('q')
    print("Execution canceled. Please wait while the script terminates")
    th1_progress = True
    th1.start()


def on_close():
    if(not th1_done):
        global th1_progress
        if(messagebox.askokcancel("Quit", "Do you want to stop Execution?")):
            if(not th1_progress):
                qu_main.put('q')
                th1_progress = True
                th1.start()
            else:
                print("Please wait for the script to End")
            return
    else:
        root.destroy()
        return


file_list = ["ISP", "servers"]

if __name__ == '__main__':

    qu_main = qu()
    root = tk.Tk()
    root.title("Ping Script GUI")
    root.geometry("700x700")

    # set window color
    root.configure(bg='white')

    text_output = tk.Text(root, wrap=tk.WORD)
    text_output.pack(fill=tk.BOTH, expand=True)

    sys.stdout.write = redirect_print  # Redirect print statements to GUI

    cancel_button = tk.Button(root, text="Cancel", command=on_cancel)
    cancel_button.place(x=250, y=470)
    cancel_button.pack()
    start_process()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
