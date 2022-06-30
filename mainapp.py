import tkinter as tk
from tkinter import ttk
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

class mainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('450x350')
        self.resizable(0, 0)
        self.title('Crypto Address Scanner')

        # UI options
        paddings = {'padx': 5, 'pady': 5}
        entry_font = {'font': ('Helvetica', 11)}

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        instance_label = ttk.Label(self, text="Instance:")

        instance_label.grid(column=0, row=0, sticky=tk.W, **paddings)
        
        username = tk.StringVar()
        password = tk.StringVar()

        # username


        username_entry = ttk.Entry(self, textvariable=username, **entry_font)
        username_entry.grid(column=1, row=0, sticky=tk.E, **paddings)

        # password
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=0, row=1, sticky=tk.W, **paddings)

        password_entry = ttk.Entry(
            self, textvariable=password, show="*", **entry_font)
        password_entry.grid(column=1, row=1, sticky=tk.E, **paddings)

        # login button
        login_button = ttk.Button(self, text="Login")
        login_button.grid(column=1, row=3, sticky=tk.E, **paddings)

        # configure style
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica', 11))
        self.style.configure('TButton', font=('Helvetica', 11))
