from tournament_gui import SchedulerGUI
from tournament_data import TournamentData
from tournament_logic import TournamentLogic

from loadui import LoadUI

def main(schedule_name, tournament_dict):
    data = TournamentData(tournament_dict["path"], tournament_dict["player_list"], tournament_dict["initial_rank"])
    schedule = TournamentLogic(tournament_data=data)
    ui = SchedulerGUI(schedule_name,
                      tournament_logic=schedule,
                      tournament_data=data)
    ui.mainloop()

if __name__ == "__main__":
    load_ui = LoadUI(command=main)
    load_ui.mainloop()
  
