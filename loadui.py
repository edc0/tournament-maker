import tkinter as tk
from tkinter import filedialog
import os
import json
from functools import partial
import pandas
from appdirs import *

APP_NAME = "BikepoloApp"
PATH = user_data_dir(APP_NAME)
print(f"using {PATH} as data storage dir!! all the relevant files are there.")
TOURNAMENTS_FILE = os.path.join(PATH, "tournaments.json")
CONFIG_FILE = os.path.join(PATH, "config.toml")

class LoadUI(tk.Tk):
    def __init__(self, command):
        super().__init__()
        if not os.path.exists(PATH):
            os.makedirs(PATH)

        if not os.path.exists(CONFIG_FILE):
            print("did not find config file")
            config = "[rating]\nwin = 3\ntie = 1\nloss = 0\n\n[mode]\nmode = 'abc' # or 'random'"
            with open(CONFIG_FILE, "w") as file:
                file.write(config)
                file.close()
        else:
            print("config file found. loading.")

        self.command = command
        self.initialize()

    def initialize(self):
        self.tournament_dict = load_tournament_filepaths(TOURNAMENTS_FILE)
        if self.tournament_dict == None:
            self.tournament_dict = {}
            self.new_tournament()            
        else:
            self.listbox = tk.Listbox(self, width=40)
            self.listbox.grid(row=0, column=0)

            for item in self.tournament_dict:
                self.listbox.insert(tk.END, item)
            
            self.button_load = tk.Button(self, text="LOAD", command=partial(self.close_and_load, self.command))
            self.button_load.grid(row=1, column=0)

            self.button_new = tk.Button(self, text="NEW", command=self.destroy_widgets_and_new_tournament)
            self.button_new.grid(row=2, column=0)

    def close_and_load(self, command):
        schedule = self.listbox.curselection()
        if len(schedule) == 0:
            return
        schedule = self.listbox.get(schedule[0])
        self.destroy()
        self.command(schedule, self.tournament_dict[schedule])
    
    def new_tournament(self):
        self.label = tk.Label(self, text="Tournament Name: ")
        self.label.grid(row=0, column=0)
        self.entry = tk.Entry()
        self.entry.grid(row=0, column=1)
        
        self.label3 = tk.Label(self, text="Player List Path: ")
        self.label3.grid(row=2, column=0)
        self.player_path = tk.StringVar()
        self.entry3 = tk.Entry(textvariable=self.player_path)
        self.entry3.grid(row=2, column=1)
        self.button3 = tk.Button(text="Search", command=partial(self.dialog, self.player_path))
        self.button3.grid(row=2, column=2)

        self.button = tk.Button(text="Apply", command=self.apply)
        self.button.grid(row=3, column=0)
    
    def destroy_widgets_and_new_tournament(self):
        self.listbox.destroy()
        self.button_load.destroy()
        self.button_new.destroy()
        self.new_tournament()

    def destroy_new_tournament_widgets(self):
        self.label.destroy()
        self.entry.destroy()
        self.label3.destroy()
        self.entry3.destroy()
        self.button3.destroy()
        self.button.destroy()

    def apply(self):
        name = str(self.entry.get())
        path = f"{os.getcwd()}/{name}"
        path = path if not os.path.exists(path) else f"{path}_new"
        player_list_raw = pandas.read_csv(self.player_path.get(), header=None)
        print("PLAYER LIST:")
        print(player_list_raw)
        player_list = player_list_raw[0].to_list()
        initial_rank = player_list_raw[1].to_list()
        self.tournament_dict[name] = {"path": path, "player_list": player_list, "initial_rank": initial_rank}
        with open(TOURNAMENTS_FILE, 'w') as outfile:
            json.dump(self.tournament_dict, outfile)
        self.destroy_new_tournament_widgets()
        self.initialize()


    def dialog(self, string_var):
        filename =  filedialog.askopenfilename(
            initialdir = os.path.realpath(__file__), 
            title = "Select a File",
            filetypes = (("CSV files", "*.csv*"),))
        string_var.set(filename)



def load_tournament_filepaths(fp):
    if not os.path.exists(os.path.relpath(fp)):
        return None
    else:
        with open(fp) as json_file:
            data = json.load(json_file)
        return data


