import tkinter as tk
from tkinter import ttk
from logic import SUB
import logic
from scrollframe import ScrollFrame
from functools import partial


def naming(player):
    if player != None:
        return player["name"]
    else:
        return SUB

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
    def __init__(self, master=None, games=[], round_number=1):
        super().__init__(master)
        self.master = master
        self.game_rows = []
        self.games = games
        self.round_number = round_number
        self.create_widgets(self.games, round_number=self.round_number)

    def create_widgets(self, games, round_number=1):
        self.games = games
        self.round_number = round_number
        self.label = tk.Label(self, text=f"ROUND #{round_number}")
        self.label.grid(row=0)
        self.frame = tk.Frame(self)
        self.frame.grid(row=1)
        for row, game in enumerate(self.games):
            self.create_game_row(game, row=row+1)


    def set_round_number(self, round_number):
        self.round_number = round_number
        self.update_label_round_number()

    def update_label_round_number(self):
        self.label.config(text=f"ROUND #{self.round_number}")


    def create_game_row(self, game, row=0):
        player1team1 = ttk.Label(self.frame, width=10)
        player1team1.grid(row=row, column=0)
        player2team1 = ttk.Label(self.frame, width=10)
        player2team1.grid(row=row, column=1)
        player3team1 = ttk.Label(self.frame, width=10)
        player3team1.grid(row=row, column=2)
        goals_team1 = tk.Entry(self.frame, validate="all", validatecommand=(self.master.register(callback), "%P"), width=3)
        goals_team1.grid(row=row, column=3)
        center_label = tk.Label(self.frame, text=":", width=1)
        center_label.grid(row=row, column=4)
        goals_team2 = tk.Entry(self.frame, validate="all", validatecommand=(self.master.register(callback), "%P"), width=3)
        goals_team2.grid(row=row, column=5)
        player1team2 = ttk.Label(self.frame, width=10)
        player1team2.grid(row=row, column=6)
        player2team2 = ttk.Label(self.frame, width=10)
        player2team2.grid(row=row, column=7)
        player3team2 = ttk.Label(self.frame, width=10)
        player3team2.grid(row=row, column=8)

        # Loads goals of the game
        if game[2] != None:
            goals_team1.insert(0, str(game[2][0]))
            goals_team2.insert(0, str(game[2][1]))

        player1team1.config(text=naming(game[0][0]))
        player2team1.config(text=naming(game[0][1]))
        player3team1.config(text=naming(game[0][2]))
        player1team2.config(text=naming(game[1][0]))
        player2team2.config(text=naming(game[1][1]))
        player3team2.config(text=naming(game[1][2]))

        self.game_rows.append([player1team1, player2team1, player3team1,
                               goals_team1, center_label, goals_team2,
                               player1team2, player2team2, player3team2])

    def set_game_row(self, game_row, game):
        game_row[0].config(text=naming(game[0][0]))
        game_row[1].config(text=naming(game[0][1]))
        game_row[2].config(text=naming(game[0][2]))
        if game[2] == None:
            game_row[3].delete(0, tk.END)
            game_row[5].delete(0, tk.END)
        else:
            game_row[3].insert(0, str(game[2][0])) # Sets the score if avaiable
            game_row[5].insert(0, str(game[2][1]))
        game_row[6].config(text=naming(game[1][0]))
        game_row[7].config(text=naming(game[1][1]))
        game_row[8].config(text=naming(game[1][2]))


    def delete_game_row(self, index=None):
        if index == None:
            index = len(self.game_rows)-1
        for widget in self.game_rows[index]:
            widget.destroy()
        del self.game_rows[index]

    def add_game_row(self, game):
        self.create_game_row(game, row=len(self.game_rows)+1)

    def update(self, games, players_not_in_schedule, round_number):
        self.set_round_number(round_number)

        while len(games) < len(self.game_rows):
            self.delete_game_row()
        while len(games) > len(self.game_rows):
            self.add_game_row(games[-1*(len(games)-len(self.game_rows))])
        
        self.games = games
        for i, game in enumerate(self.games):
            self.set_game_row(self.game_rows[i], game)         


    def all_games_played(self):
        for i, (_, _, _, e1, _, e2, _, _, _) in enumerate(self.game_rows):
            if e1.get() == "" or e2.get() == "":
                return False
            else:
                self.games[i][2] = [parse_string_to_int(e1.get()), parse_string_to_int(e2.get())]
        return True

CHECKBOX = 0
PLAYER = 1
class RankFrame(ScrollFrame):
    def __init__(self, master=None, player_list=None):
        super().__init__(master)
        self.ranking_list_labels = []
        self.create_widgets(player_list)
      

    def create_widgets(self, player_list):
        tk.Label(self.viewPort, anchor=tk.W, text="RANK", width=5).grid(row=0,column=1)
        tk.Label(self.viewPort, anchor=tk.W, text="NAME", width=15).grid(row=0,column=2)
        tk.Label(self.viewPort, anchor=tk.W, text="WINS", width=5).grid(row=0,column=3)
        tk.Label(self.viewPort, anchor=tk.W, text="LOSSES", width=5).grid(row=0,column=4)
        tk.Label(self.viewPort, anchor=tk.W, text="TIES", width=5).grid(row=0,column=5)
        tk.Label(self.viewPort, anchor=tk.W, text="GAMES", width=5).grid(row=0,column=6)
        tk.Label(self.viewPort, anchor=tk.W, text="ΔGOAL", width=5).grid(row=0,column=7)
        tk.Label(self.viewPort, anchor=tk.W, text="POINTS", width=6).grid(row=0,column=8)

        if player_list == None:
            return
        
        for i, player in enumerate(player_list):
            row = self.create_player_row(i, player)
            self.ranking_list_labels.append(row)

    def delete_player_row(self):
        pass

    def create_player_row(self, index, player):
        row = {}
        color = ("lightgray" if index % 2 != 0 else "#FFFFFF")
        var = tk.IntVar()
        row["var"] = var
        row["in_schedule"] = tk.Checkbutton(self.viewPort, bg=color, variable=row["var"], command=partial(self.update_row, index, player, update_by=CHECKBOX))
        row["in_schedule"].select() if bool(player["in_schedule"]) else row["in_schedule"].deselect()
        row["in_schedule"].grid(row=index+1, column=0)
        row["rank"] = tk.Label(self.viewPort, anchor=tk.E, text=index+1, width=5, bg=color)
        row["rank"].grid(row=index+1,column=1)
        row["name"] = tk.Label(self.viewPort, anchor=tk.W, text=player["name"], width=15, bg=color)
        row["name"].grid(row=index+1,column=2)
        row["wins"] = tk.Label(self.viewPort, anchor=tk.E, text=player["wins"], width=5, bg=color)
        row["wins"].grid(row=index+1,column=3)
        row["loss"] = tk.Label(self.viewPort, anchor=tk.E, text=player["loss"], width=5, bg=color)
        row["loss"].grid(row=index+1,column=4)
        row["ties"] = tk.Label(self.viewPort, anchor=tk.E, text=player["ties"], width=5, bg=color)
        row["ties"].grid(row=index+1,column=5)
        row["played_games"] = tk.Label(self.viewPort, anchor=tk.E, text=player["played_games"], width=5, bg=color)
        row["played_games"].grid(row=index+1,column=6)
        row["goal_diff"] = tk.Label(self.viewPort, anchor=tk.E, text=player["goal_diff"], width=5, bg=color)
        row["goal_diff"].grid(row=index+1,column=7)
        row["points"] = tk.Label(self.viewPort, anchor=tk.E, text=player["points"], width=6, bg=color)
        row["points"].grid(row=index+1,column=8)
        return row

    def add_player_row(self, player):
        index = len(self.ranking_list_labels)
        self.create_player_row(index, player)

    def update_in_schedule(self, index, player):
        self.ranking_list_labels[index]["in_schedule"].config(
            command=partial(self.update_row, index, player))

        #if player["in_schedule"]:
        #    self.ranking_list_labels[index]["in_schedule"].select()
        #else:
        #    self.ranking_list_labels[index]["in_schedule"].deselect()

    def update_row(self, index, player, update_by=CHECKBOX):
        if update_by == CHECKBOX:
            if self.ranking_list_labels[index]["var"].get() == 1:
                textcolor = "black"
                player["in_schedule"] = True
            else:
                textcolor = "gray"
                player["in_schedule"] = False
            self.update_row_coloring(index, player, color=textcolor)

        if update_by == PLAYER:
            if player["in_schedule"]:
                self.update_in_schedule(index, player)
                self.update_row_coloring(index, player, color="black")
                self.ranking_list_labels[index]["in_schedule"].select()
            else:
                self.update_in_schedule(index, player)
                self.update_row_coloring(index, player, color="gray")
                self.ranking_list_labels[index]["in_schedule"].deselect()
    
    def update_row_coloring(self, index, player, color="black"):
        self.ranking_list_labels[index]["rank"].config(fg=color)
        self.ranking_list_labels[index]["name"].config(text=player["name"], fg=color)
        self.ranking_list_labels[index]["wins"].config(text=player["wins"], fg=color)
        self.ranking_list_labels[index]["ties"].config(text=player["ties"], fg=color)
        self.ranking_list_labels[index]["loss"].config(text=player["loss"], fg=color)
        self.ranking_list_labels[index]["played_games"].config(text=player["played_games"], fg=color)
        self.ranking_list_labels[index]["points"].config(text=player["points"], fg=color)
        self.ranking_list_labels[index]["goal_diff"].config(text=player["goal_diff"], fg=color)

    def update(self, player_list):
        for i, player in enumerate(player_list):
            self.update_row(i, player, update_by=PLAYER)

class PlayerInformationFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.label = tk.Label(self, text="Player")
        self.label.grid()

class SchedulerGUI(tk.Tk):
    def __init__(self, title, player_list):
        super().__init__()
        self.frame_left = tk.Frame(self)
        self.frame_left.pack(side="left", fill="both", expand=True)
        self.round_frame = RoundFrame(self.frame_left)
        self.round_frame.pack(side="top")
        self.rank_frame = RankFrame(self)
        self.rank_frame.pack(side="right", fill="both", expand=True)
        self.player_info_frame = PlayerInformationFrame(self.frame_left)
        self.player_info_frame.pack(side="bottom")

        self.tool_bar_frame = tk.Frame(self.frame_left)
        self.tool_bar_frame.pack(side="bottom")
        self.button_next_round = tk.Button(self.tool_bar_frame, text="Next Round", command=partial(self.next_round, player_list))
        self.button_next_round.grid(row=0, column=0)
        self.init_schedule(player_list)

    def next_round(self, player_list):
        if self.round_frame.all_games_played():
            self.round_number += 1

            logic.update_schedule(self.round_frame.games, self.round_number)
            logic.rank_player_list(player_list)

            teams, not_in_schedule = logic.get_new_teams(player_list)
            games = logic.get_new_round(teams)
            games = [game + [None] for game in games]
            
            self.round_frame.update(games=games, players_not_in_schedule=not_in_schedule, round_number=self.round_number)
            self.rank_frame.update(player_list=player_list)
    
    def init_schedule(self, player_list):
        self.round_number = 1
        teams, not_in_schedule = logic.get_new_teams(player_list)
        games = logic.get_new_round(teams)

        self.round_frame.create_widgets([game + [None] for game in games], round_number=self.round_number)
        self.rank_frame.create_widgets(player_list)

    def load_schedule(self, path):
        pass
