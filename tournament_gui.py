import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
from scrollframe import ScrollFrame
from functools import partial
import math

from tournament_data import TournamentData
from tournament_logic import TournamentLogic

def callback(P):
    if len(P) <= 2 and (str.isdigit(P) or P == ""):
        return True
    else:
        return False

def parse_string_to_int(s):
    while len(s) > 1 and s.startswith("0"):
        s = s[1:]
    return int(s)


class RoundFrame(tk.Frame):
    def __init__(self, master, tournament_data: TournamentData, round_num):
        super().__init__(master)
        self.master = master
        self.tournament_data = tournament_data
        self.game_rows = []
        self.round_num = round_num
        self.create_widgets(self.tournament_data.get_game_ids(self.round_num))

    def create_widgets(self, game_ids):
        self.frame = tk.Frame(self)
        self.frame.grid(row=0)
        for row, game_id in enumerate(game_ids):
            self.create_game_row(game_id, row=row+1)

    def create_game_row(self, game_id, row=1):
        player1team1 = ttk.Label(self.frame, width=15, state="readonly")
        player1team1.grid(row=row, column=0)
        player2team1 = ttk.Label(self.frame, width=15, state="readonly")
        player2team1.grid(row=row, column=1)
        player3team1 = ttk.Label(self.frame, width=15, state="readonly")
        player3team1.grid(row=row, column=2)
        goals_team1 = ttk.Entry(self.frame, validate="all", validatecommand=(self.master.register(callback), "%P"), width=3)
        goals_team1.grid(row=row, column=3)
        center_label = ttk.Label(self.frame, text=":", width=1)
        center_label.grid(row=row, column=4)
        goals_team2 = ttk.Entry(self.frame, validate="all", validatecommand=(self.master.register(callback), "%P"), width=3)
        goals_team2.grid(row=row, column=5)
        player1team2 = ttk.Label(self.frame, width=15, state="readonly")
        player1team2.grid(row=row, column=6)
        player2team2 = ttk.Label(self.frame, width=15, state="readonly")
        player2team2.grid(row=row, column=7)
        player3team2 = ttk.Label(self.frame, width=15, state="readonly")
        player3team2.grid(row=row, column=8)
        applybutton = ttk.Button(self.frame, text="Apply", width=8, command=partial(self.apply, row-1))
        applybutton.grid(row=row, column=9)

        # Loads goals of the game
        goals1, goals2 = self.tournament_data.get_game_result(game_id)
        if not (math.isnan(goals1) or math.isnan(goals2)):
            goals_team1.insert(0, str(int(goals1)))
            goals_team2.insert(0, str(int(goals2)))

        player1team1['text'] = (self.tournament_data.get_name_of_player1(self.tournament_data.get_team1_id(game_id)))
        player2team1['text'] = (self.tournament_data.get_name_of_player2(self.tournament_data.get_team1_id(game_id)))
        player3team1['text'] = (self.tournament_data.get_name_of_player3(self.tournament_data.get_team1_id(game_id)))
        player1team2['text'] = (self.tournament_data.get_name_of_player1(self.tournament_data.get_team2_id(game_id)))
        player2team2['text'] = (self.tournament_data.get_name_of_player2(self.tournament_data.get_team2_id(game_id)))
        player3team2['text'] = (self.tournament_data.get_name_of_player3(self.tournament_data.get_team2_id(game_id)))

        self.game_rows.append([player1team1, player2team1, player3team1,
                               goals_team1, goals_team2,
                               player1team2, player2team2, player3team2,
                               applybutton, game_id])

    def write_game_result(self, game_id, goals_team1_entry, goals_team2_entry):
        self.tournament_data.set_game_result(game_id, int(goals_team1_entry.get()), int(goals_team2_entry.get()))
        self.master.update()
        self.tournament_data.save_tournament()

    def disable(self):
        for i, row in enumerate(self.game_rows):
            for item in row[:-2]:
                item.config(state='disabled')
            row[-2].config(text="Edit", command=partial(self.enable_row, i))

    def enable_row(self, row_index):
        row = self.game_rows[row_index]
        for item in row[:-2]:
            item.config(state='readonly')
        row[3].config(state='normal')
        row[4].config(state='normal')
        row[-2].config(text="Update", command=partial(self.disable_row, row_index))

    def disable_row(self, row_index):
        row = self.game_rows[row_index]
        for item in row[:-2]:
            item.config(state='disabled')
        row[-2].config(text="Edit", command=partial(self.enable_row, row_index))
        self.write_game_result(row[-1], row[3], row[4])


    def apply(self, row_index):
        row = self.game_rows[row_index]

        if row[3].get() != "" and row[4].get() != "":
            self.disable_row(row_index)
            self.write_game_result(row[-1], row[3], row[4])

CHECKBOX = 0
PLAYER = 1
class RankFrame(ScrollFrame):
    def __init__(self, master, tournament_data: TournamentData):
        super().__init__(master)
        self.master = master
        self.tournament_data = tournament_data
        self.ranking_list_labels = []
        self.create_widgets()
      

    def create_widgets(self):
        tk.Label(self.viewPort, anchor=tk.W, text="RANK", width=5).grid(row=0,column=1)
        tk.Label(self.viewPort, anchor=tk.W, text="NAME", width=15).grid(row=0,column=2)
        tk.Label(self.viewPort, anchor=tk.W, text="WINS", width=5).grid(row=0,column=3)
        tk.Label(self.viewPort, anchor=tk.W, text="LOSSES", width=5).grid(row=0,column=4)
        tk.Label(self.viewPort, anchor=tk.W, text="TIES", width=5).grid(row=0,column=5)
        tk.Label(self.viewPort, anchor=tk.W, text="GAMES", width=5).grid(row=0,column=6)
        tk.Label(self.viewPort, anchor=tk.W, text="ΔGOAL", width=5).grid(row=0,column=7)
        tk.Label(self.viewPort, anchor=tk.W, text="POINTS", width=6).grid(row=0,column=8)
        
        ranking = self.tournament_data.calculate_ranking()
        for i, player in enumerate(ranking.index):
            self.add_player_row(ranking=ranking,
                                player_id=player,
                                player_activity=self.tournament_data.get_player_activity(player, self.master.round_num),
                                index=i)

    def delete_all_player_rows(self):
        for row in self.ranking_list_labels:
            row["in_schedule"].destroy()
            row["rank"].destroy()
            row["name"].destroy()
            row["wins"].destroy()
            row["loss"].destroy()
            row["ties"].destroy()
            row["played_games"].destroy()
            row["goal_diff"].destroy()
            row["points"].destroy()
        self.ranking_list_labels = []

    def _create_player_row(self, ranking, player_id, player_activity, index):
        row = {}
        color = ("lightgray" if index % 2 != 0 else "#FFFFFF")
        fcolor = "black" if player_activity["ACTIVE"] else "gray"
        var = tk.IntVar()
        row["var"] = var
        row["in_schedule"] = ttk.Checkbutton(self.viewPort, bg=color, variable=row["var"], command=partial(self.update_row, index, player_id))
        row["in_schedule"].select() if bool(player_activity["ACTIVE"]) else row["in_schedule"].deselect()
        row["in_schedule"].grid(row=index+1, column=0)
        row["rank"] = ttk.Label(self.viewPort, anchor=tk.E, text=index+1, width=5, bg=color, fg=fcolor)
        row["rank"].grid(row=index+1,column=1)
        row["name"] = ttk.Label(self.viewPort, anchor=tk.W, text=ranking.loc[player_id]['PLAYER_NAME'], width=15, bg=color, fg=fcolor)
        row["name"].grid(row=index+1,column=2)
        row["wins"] = ttk.Label(self.viewPort, anchor=tk.E, text=ranking.loc[player_id]["WINS"], width=5, bg=color, fg=fcolor)
        row["wins"].grid(row=index+1,column=3)
        row["loss"] = ttk.Label(self.viewPort, anchor=tk.E, text=ranking.loc[player_id]["LOSSES"], width=5, bg=color, fg=fcolor)
        row["loss"].grid(row=index+1,column=4)
        row["ties"] = ttk.Label(self.viewPort, anchor=tk.E, text=ranking.loc[player_id]["TIES"], width=5, bg=color, fg=fcolor)
        row["ties"].grid(row=index+1,column=5)
        row["played_games"] = ttk.Label(self.viewPort, anchor=tk.E, text=ranking.loc[player_id]["PLAYED_GAMES"], width=5, bg=color, fg=fcolor)
        row["played_games"].grid(row=index+1,column=6)
        row["goal_diff"] = ttk.Label(self.viewPort, anchor=tk.E, text=ranking.loc[player_id]["GOALDIFF"], width=5, bg=color, fg=fcolor)
        row["goal_diff"].grid(row=index+1,column=7)
        row["points"] = ttk.Label(self.viewPort, anchor=tk.E, text=ranking.loc[player_id]["POINTS"], width=6, bg=color, fg=fcolor)
        row["points"].grid(row=index+1,column=8)
        return row

    def update(self):
        self.delete_all_player_rows()
        self.create_widgets()

    def add_player_row(self, ranking, player_id, player_activity, index=None):
        if index == None:
            index = len(self.ranking_list_labels)
        row = self._create_player_row(ranking, player_id, player_activity, index)
        self.ranking_list_labels.append(row)

    def update_row(self, index, player_id):
        if self.ranking_list_labels[index]["var"].get() == 1:
            textcolor = "black"
            self.tournament_data.set_player_active(player_id, self.master.round_num)
        else:
            textcolor = "gray"
            self.tournament_data.set_player_inactive(player_id, self.master.round_num)
        self.update_row_coloring(index, color=textcolor)
    
    def update_row_coloring(self, index, color="black"):
        self.ranking_list_labels[index]["rank"].config(fg=color)
        self.ranking_list_labels[index]["name"].config(fg=color)
        self.ranking_list_labels[index]["wins"].config(fg=color)
        self.ranking_list_labels[index]["ties"].config(fg=color)
        self.ranking_list_labels[index]["loss"].config(fg=color)
        self.ranking_list_labels[index]["played_games"].config(fg=color)
        self.ranking_list_labels[index]["points"].config(fg=color)
        self.ranking_list_labels[index]["goal_diff"].config(fg=color)


class PlayerInformationFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)


class SchedulerGUI(tk.Tk):
    def __init__(self, title, tournament_logic: TournamentLogic, tournament_data: TournamentData):
        super().__init__()
        
        self.notebook_round_frames = []
        self.tournament_logic = tournament_logic
        self.tournament_data = tournament_data

        self.frame_left = tk.Frame(self)
        self.frame_left.pack(side="left", fill="both", expand=True)
        self.notebook = ttk.Notebook(self.frame_left)
        self.notebook.pack(side="top")

        self.initialize()

        self.rank_frame = RankFrame(self, tournament_data)
        self.rank_frame.pack(side="right", fill="both", expand=True)

        self.player_info_frame = PlayerInformationFrame(self.frame_left)
        self.player_info_frame.pack(side="bottom")

        self.tool_bar_frame = tk.Frame(self.frame_left)
        self.tool_bar_frame.pack(side="bottom")
        self.button_next_round = ttk.Button(self.tool_bar_frame, text="Next Round", command=partial(self.next_round))
        self.button_next_round.grid(row=0, column=0)
    
    def create_round_frame(self, round_num):
        round_frame = RoundFrame(self, self.tournament_data, round_num)
        self.notebook_round_frames.append(round_frame)

        self.notebook.add(round_frame, text=f"Round {round_num+1}")
        self.notebook.select(round_frame)
        self.notebook.enable_traversal()

    def next_round(self):
        if self.round_num == 0 and len(self.tournament_data.get_game_ids(self.round_num)) == 0:
            self.tournament_logic.next_round(self.round_num)
            self.create_round_frame(self.round_num)
        elif not self.tournament_data.all_games_played(self.round_num):
            return
        else:
            self.round_num += 1
            self.tournament_logic.next_round(self.round_num)
            for round_frame in self.notebook_round_frames:
                round_frame.disable()
                continue
            self.create_round_frame(self.round_num)
            self.rank_frame.update()
    
    def initialize(self):
        for round_num in range(self.tournament_data.get_round_numbers()):
            self.round_num = round_num
            self.create_round_frame(round_num)
        for round_frame in self.notebook_round_frames[:-1]:
            round_frame.disable()
        
        if self.tournament_data.get_round_numbers() == 0:
            self.round_num = 0

    def update(self):
        self.rank_frame.update()

    def load_schedule(self, path):
        pass
