import tkinter as tk
import sys
from tkinter import ttk
#import ansi
'''
screen elements
title,
+/- instances
Instance name, 
run count, 
winners count,
speed,
winners list

start / stop buttons
'''
default_btc_instances = 2
default_eth_instances = 2


class mainApp():
    # root window
    root = tk.Tk()
    root.geometry("440x300")
    root.title('Crypto Scanner')
    root.resizable(0, 0)
    btc_instances = default_btc_instances
    eth_instances = default_eth_instances
    btc_status = []
    eth_status = []

    row = 0
    top_menu_frame = None
    cryto_status_frame = None

    def __init__(self):
        self.draw_screen()

    def mainloop(self):
        self.root.mainloop()

    def draw_screen(self):
        self.row = 0
        self.top_menu()
        self.btc_status = CryptoStatus(self.root, "btc", default_btc_instances)
        self.eth_status = CryptoStatus(self.root, "eth", default_eth_instances)

    def top_menu(self):
        self.top_menu_frame = tk.Frame(self.root)
        #top_menu_frame.configure(width = 440)
        self.top_menu_frame.columnconfigure(0, weight=0)
        self.top_menu_frame.columnconfigure(1, weight=0)
        self.top_menu_frame.columnconfigure(2, weight=0)
        self.top_menu_frame.columnconfigure(3, weight=100)
        self.top_menu_frame.pack(side=tk.TOP, fill="x")
        padx = 2
        pady = 5

        # row 0 - controls
        btc_button = ttk.Button(self.top_menu_frame, text="Start BTC")

        btc_button.grid(column=0,
                        row=self.row,
                        sticky=tk.NW,
                        padx=padx,
                        pady=pady)

        eth_button = ttk.Button(self.top_menu_frame, text="Start ETH")
        eth_button.grid(column=1,
                        row=self.row,
                        sticky=tk.NW,
                        padx=padx,
                        pady=pady)

        quit_button = ttk.Button(self.top_menu_frame,
                                 text="Quit",
                                 command=sys.exit)
        quit_button.grid(column=2,
                         row=self.row,
                         sticky=tk.NW,
                         padx=padx,
                         pady=pady)


class CryptoStatus():
    coin = ""
    instances = 1
    max_instances = 5
    text_label_prefix = None
    text_label = None
    plus_button = None
    status_frame = None
    status_text = []
    cryto_status_frame = None
    initialized = False
    process_status_text = []

    def __init__(self, root, coin, instances):
        self.coin = coin
        self.set_instances(instances)

        for x in range(0, self.max_instances):
            self.status_text.append(None)
            self.process_status_text.append("No process running")

        # create frame
        self.cryto_status_frame = tk.Frame(root)
        self.cryto_status_frame.configure(width=440)
        self.cryto_status_frame.columnconfigure(0, weight=1)
        self.cryto_status_frame.columnconfigure(1, weight=1)
        self.cryto_status_frame.columnconfigure(2, weight=1)
        self.cryto_status_frame.columnconfigure(3, weight=100)
        self.cryto_status_frame.pack(side=tk.TOP, fill="x")

        # create widgets in frame
        self.set_label()
        self.set_buttons()
        self.show_process_list()

        self.initialized = True

    def set_label(self):
        try:
            self.text_label = ttk.Label(self.cryto_status_frame,
                                        text=self.text_label_prefix)
            self.text_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        except:
            self.text_label.config(text=self.text_label_prefix)



























            
    def set_process_status_text(self, id, msg):
        self.process_status_text[id] = msg
        self.show_process_list()
        
    def show_process_list(self):
        try:
            self.process_list = tk.Frame(self.cryto_status_frame)
            self.process_list.configure(width=440)
            self.process_list.columnconfigure(0, weight=100)
            self.cryto_status_frame.pack(side=tk.TOP, fill="x")

        except:
            pass

        for i in range(0, self.max_instances):
            self.status_text[i] = ttk.Label(self.cryto_status_frame,
                                            text=" " * 200)
            self.status_text[i].grid(column=0,
                                     columnspan=4,
                                     row=i + 1,
                                     sticky=tk.W,
                                     padx=5,
                                     pady=1)

        for i in range(0, self.instances):
            self.status_text[i] = ttk.Label(
                self.cryto_status_frame,
                text=self.process_status_text[i])
            self.status_text[i].grid(column=0,
                                     columnspan=4,
                                     row=i + 1,
                                     sticky=tk.W,
                                     padx=5,
                                     pady=1)

    def set_buttons(self):
        self.plus_button = ttk.Button(self.cryto_status_frame,
                                      text="+",
                                      width=1,
                                      command=self.more_instances)
        self.plus_button.grid(column=1, row=0, sticky=tk.W, padx=1, pady=1)

        self.minus_button = ttk.Button(self.cryto_status_frame,
                                       text="-",
                                       width=1,
                                       command=self.less_instances)
        self.minus_button.grid(column=2, row=0, sticky=tk.W, padx=1, pady=1)

    def more_instances(self):
        self.set_instances(1)

    def less_instances(self):
        self.set_instances(-1)

    def set_instances(self, adjust):
        instances = self.instances + adjust
        if instances < 1:
            instances = 1
        if instances > self.max_instances:
            instances = self.max_instances

        self.instances = instances
        self.text_label_prefix = f"{self.coin.upper()} ({instances})"
        self.set_label()
        if self.initialized:
            self.show_process_list()
