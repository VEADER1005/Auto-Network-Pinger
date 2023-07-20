import os
import pandas as pd
import sys
import time
import keyboard
from threading import Thread
from queue import Queue as qu


# def open_file(file_name):
#     with open("D:/Network/"+file_name) as file:
#         park = file.read()
#         park = park.splitlines()
#         check(park)
#     return
def start():
    for file_name in file_list:
        unrechable = []
        rechable = []
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
            print(response)
            unrechable.append(str(col_IP[ip] + " at " + col_name[ip]))
        else:
            print(response)
            rechable.append(str(col_IP[ip] + " at " + col_name[ip]))
    return


def main1():
    print("main has been called")
    while(True):
        x = 0
        print("start will be called")
        start()
        print("Starting Sleep Cycle")
        while(x < 7200):
            if(not qu_main.empty()):
                if(qu_main.get() == 'q'):
                    print("ending the Cycle")
                    return
                else:
                    print("sleep")
                    x += 1
                    time.sleep(1)
            else:
                print("sleep")
                x += 1
                time.sleep(1)


def qu1():
    while(True):
        if keyboard.is_pressed("q"):
            qu_main.put("q")
            print("added q")
            break
        else:
            pass
    return


file_list = ["ISP", "servers", "NVR"]

if __name__ == '__main__':

    qu_main = qu()
    th1 = Thread(target=qu1)
    th1.start()

    th2 = Thread(target=main1)
    th2.start()

    # if keyboard.is_pressed("q"):
    #     qu_main.put("q")
    # else:
    #     pass


# for file_name in file_list:
#     print(file_name)
#     open_file(file_name)
# for file_name in file_list:
#     print(file_name)
#     open_file(file_name)
