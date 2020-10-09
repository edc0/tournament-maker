import json
import os
from tkinter import filedialog

from tournament_gui import SchedulerGUI
from tournament_data import TournamentData
from tournament_logic import TournamentLogic

from loadui import LoadUI

def main(schedule_name, tournament_dict):
    data = TournamentData(tournament_dict["path"], tournament_dict["player_list"])
    schedule = TournamentLogic(tournament_data=data)
    ui = SchedulerGUI(schedule_name,
                      tournament_logic=schedule,
                      tournament_data=data)
    ui.mainloop()

if __name__ == "__main__":
    player_keys = ["Rafael DÜS", "Moggi DUI", "Ben MÜ","Patrick BRÜ", "Frank HAN",
    "Aislan GRO", "Markus HAN", "Julius HAL", "Holger ALA", "Thommy HAN", "Aljoscha BER"]# "Christoph LEI", "Markus BER", "Richie LEI", "Emílio D. C. BER",
    #"Max CAM"]
    # "Florian GRO", "Levin HAL", "John MAN", "Oli MAN",
    #"Dima Kharkiv", "Megan AUS", "Daniel HAL", "Judith HH ", "Antonio LON", "Domi ULM",
    #"Sam ZÜR", "Thomas HAN ", "Rado FRA", "David MÜ", "Chris HH ", "Steffn HH",
    #"Fabian BÜ", "Ole BÜ", "Flo BÜ", "Johannes BÜ", "Buby BÜ", "Kai BÜ", "Andy BÜ",
    #"Franky BÜ"]
    
    load_ui = LoadUI(".tournaments.json", command=main)
    load_ui.mainloop()
  