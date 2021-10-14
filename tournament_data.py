import pandas as pd
import os
import math
import toml

class TournamentData:
    SUB = -1

    def __init__(self, path, player_list=[]):
        self.path = path
        self._load_or_new_tournament(player_list)
        self.config = toml.load("config.toml")

    def new_tournament(self, player_list):
        self.df_players = pd.DataFrame(player_list, columns=['PLAYER_NAME'])
        self.df_teams = pd.DataFrame(
            [], columns=['ROUND_NUM', 'PLAYER1_ID', 'PLAYER2_ID', 'PLAYER3_ID'])
        self.df_games = pd.DataFrame(
            [], columns=['ROUND_NUM', 'TEAM1_ID', 'TEAM2_ID', 'GOALS_TEAM1', 'GOALS_TEAM2'])
        self.df_players_activity = pd.DataFrame(
            [], columns=['ROUND_NUM', 'PLAYER_ID', 'ACTIVE'])
        self.initialize_player_round_activity()
        self.save_tournament()

    def load_tournament(self):
        self.df_players = pd.read_csv(f"{self.path}/player.csv", index_col=0)
        self.df_teams = pd.read_csv(f"{self.path}/teams.csv", index_col=0)
        self.df_games = pd.read_csv(f"{self.path}/games.csv", index_col=0)
        self.df_players_activity = pd.read_csv(
            f"{self.path}/players_activity.csv", index_col=0)

    def save_tournament(self):
        self.save_players()
        self.save_teams()
        self.save_games()
        self.save_players_activity()

    def save_players(self):
        self.df_players.to_csv(f"{self.path}/player.csv")

    def save_teams(self):
        self.df_teams.to_csv(f"{self.path}/teams.csv")

    def save_games(self):
        self.df_games.to_csv(f"{self.path}/games.csv")

    def save_players_activity(self):
        self.df_players_activity.to_csv(f"{self.path}/players_activity.csv")

    def initialize_player_round_activity(self, round_num = None):
        for player_id, _ in self.df_players.itertuples():
            if round_num == None:
                self.df_players_activity.loc[f"{player_id}R{0}"] = [
                    0, player_id, True]
            elif round_num == 0:
                continue
            else:
                activity = self.df_players_activity.loc[f"{player_id}R{round_num-1}"]["ACTIVE"]
                self.df_players_activity.loc[f"{player_id}R{round_num}"] = [
                    round_num, player_id, activity]

    def set_player_active(self, player_id, round_num):
        self.df_players_activity.loc[f"{player_id}R{round_num}"] = [
            round_num, player_id, True]

    def set_player_inactive(self, player_id, round_num):
        self.df_players_activity.loc[f"{player_id}R{round_num}"] = [
            round_num, player_id, False]

    def get_active_player_ids(self, round_num):
        df_active = self.df_players_activity.loc[self.df_players_activity["ROUND_NUM"] == round_num]
        df_active = df_active.loc[df_active["ACTIVE"] == True]
        return df_active["PLAYER_ID"].tolist()

    def get_inactive_player_ids(self, round_num):
        df_active = self.df_players_activity.loc[self.df_players_activity["ROUND_NUM"] == round_num]
        df_active = df_active.loc[self.df_players_activity["ACTIVE"] == False]
        return df_active["PLAYER_ID"].tolist()

    def get_player_activity(self, player_id, round_num):
        return self.df_players_activity.loc[f"{player_id}R{round_num}"]

    def get_round_numbers(self):
        return self.df_games["ROUND_NUM"].nunique()

    def add_player(self, player_name):
        player_id = 0 if len(
            self.df_players) == 0 else self.df_players.index.max() + 1
        self.df_players.loc[player_id] = [player_name, str(True)]
        self.save_players()
        return player_id

    def add_team(self, round_num, player1_id, player2_id, player3_id):
        team_id = 0 if len(
            self.df_teams) == 0 else self.df_teams.index.max() + 1
        self.df_teams.loc[team_id] = [
            round_num, player1_id, player2_id, player3_id]
        self.save_teams()
        return team_id

    def add_game(self, round_num, team1_id, team2_id, goals_team1=None, goals_team2=None):
        game_id = 0 if len(
            self.df_games) == 0 else self.df_games.index.max() + 1
        self.df_games.loc[game_id] = [round_num,
                                      team1_id, team2_id, goals_team1, goals_team2]
        self.save_games()
        return game_id

    def get_game_ids(self, round_num):
        return self.df_games.index[self.df_games["ROUND_NUM"] == round_num].tolist()

    def get_player_name(self, player_id):
        if player_id <= TournamentData.SUB:
            return "TBA (SUB)"
        return self.df_players.loc[player_id]["PLAYER_NAME"]

    def get_name_of_player1(self, team_id):
        return self.get_player_name(self.df_teams.loc[team_id]["PLAYER1_ID"])

    def get_name_of_player2(self, team_id):
        return self.get_player_name(self.df_teams.loc[team_id]["PLAYER2_ID"])

    def get_name_of_player3(self, team_id):
        return self.get_player_name(self.df_teams.loc[team_id]["PLAYER3_ID"])

    def get_team1_id(self, game_id):
        return self.df_games.loc[game_id]["TEAM1_ID"]

    def get_team2_id(self, game_id):
        return self.df_games.loc[game_id]["TEAM2_ID"]

    def set_game_result(self, game_id, goals_team1, goals_team2):
        self.df_games.loc[game_id, ["GOALS_TEAM1"]] = goals_team1
        self.df_games.loc[game_id, ["GOALS_TEAM2"]] = goals_team2

    def get_game_result(self, game_id):
        return self.df_games.loc[game_id]["GOALS_TEAM1"], self.df_games.loc[game_id]["GOALS_TEAM2"]

    def set_player1(self, team_id, player_id):
        self.df_teams.loc[team_id, ["PLAYER1_ID"]] = player_id

    def set_player2(self, team_id, player_id):
        self.df_teams.loc[team_id, ["PLAYER2_ID"]] = player_id

    def set_player3(self, team_id, player_id):
        self.df_teams.loc[team_id, ["PLAYER3_ID"]] = player_id

    def all_games_played(self, round_num):
        round_games = self.df_games.loc[self.df_games["ROUND_NUM"] == round_num]
        if len(round_games) == 0:
            return False
        for game in round_games.itertuples():
            # 4 and 5 are the indices for entering the results of the game
            if math.isnan(game[4]) or math.isnan(game[5]):
                return False
        return True

    def calculate_ranking(self):
        df_ranking = pd.DataFrame([], columns=[
                                  "PLAYER_NAME", "WINS", "LOSSES", "TIES", "PLAYED_GAMES", "GOALDIFF", "POINTS"])

        # Initializes the ranking list
        for player_id, player_name in self.df_players.itertuples():
            df_ranking.loc[player_id] = [player_name, 0, 0, 0, 0, 0, 0]

        # Calculates for each game the wins, losses, ties and goaldiff for each member.
        for _, _, team1_id, team2_id, goals_team1, goals_team2 in self.df_games.itertuples():
            player_IDs_team1 = self.df_teams.loc[team1_id][1:]
            player_IDs_team2 = self.df_teams.loc[team2_id][1:]
            [team1_result_identifier, team2_result_identifier] = _get_result_identifier(
                goals_team1, goals_team2)

            if team1_result_identifier == None or team2_result_identifier == None:
                continue

            for player_id in player_IDs_team1:
                if player_id != TournamentData.SUB:
                    df_ranking.loc[player_id, [team1_result_identifier]] += 1
                    df_ranking.loc[player_id, ["GOALDIFF"]
                                   ] += int(goals_team1-goals_team2)
                    df_ranking.loc[player_id, ["PLAYED_GAMES"]] += 1

            for player_id in player_IDs_team2:
                if player_id != TournamentData.SUB:
                    df_ranking.loc[player_id, [team2_result_identifier]] += 1
                    df_ranking.loc[player_id, ["GOALDIFF"]
                                   ] += int(goals_team2-goals_team1)
                    df_ranking.loc[player_id, ["PLAYED_GAMES"]] += 1

        # Calculates the points for each player
        df_ranking["POINTS"] = df_ranking["WINS"] * self.config["rating"]["win"] + df_ranking["TIES"] * self.config["rating"]["tie"] + \
            df_ranking["LOSSES"] * self.config["rating"]["loss"]

        return df_ranking.sort_values(by=['POINTS', 'GOALDIFF', 'PLAYED_GAMES', 'WINS'], ascending=[False, False, True, False])

    def _load_or_new_tournament(self, player_list=[]):
        if os.path.exists(self.path):
            self.load_tournament()
        else:
            os.mkdir(self.path)
            self.new_tournament(player_list)


def _get_result_identifier(goals_team1, goals_team2) -> [str, str]:
    if math.isnan(goals_team1) or math.isnan(goals_team2):
        return None, None
    result = goals_team1-goals_team2
    team1_result = None
    team2_result = None
    if result == 0:
        team1_result = "TIES"
        team2_result = "TIES"
    elif result < 0:
        team1_result = "LOSSES"
        team2_result = "WINS"
    else:
        team1_result = "WINS"
        team2_result = "LOSSES"
    return team1_result, team2_result
