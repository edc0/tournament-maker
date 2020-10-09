from tournament_data import TournamentData
import random

class TournamentLogic:
    def __init__(self, tournament_data: TournamentData):
        self.tournament_data = tournament_data

    def next_round(self, round_num):
        if round_num > 0 and not self.tournament_data.all_games_played(round_num-1):
            return
        df_ranking = self.tournament_data.calculate_ranking()
        self.tournament_data.initialize_player_round_activity(round_num)
        
        self.tournament_data.save_tournament()
        
        active_players_indices = self.tournament_data.get_active_player_ids(round_num)
        
        df_active_ranking = df_ranking.loc[df_ranking.index.isin(active_players_indices)]
        teams = self._get_new_teams(df_active_ranking)
        for player1_id, player2_id, player3_id in teams:
            self.tournament_data.add_team(round_num, player1_id, player2_id, player3_id)

        games = self._get_new_games(self.tournament_data.df_teams, round_num)
        for team1_id, team2_id in games:
            self.tournament_data.add_game(int(round_num), int(team1_id), int(team2_id))

    def _get_new_teams(self, df_ranking):
        player_num = len(df_ranking)
        if player_num < 6:
            raise Exception("Not enough active players for playing next round!")

        if player_num == 7:
            raise Exception("Active player number must not be 7.")

        if player_num % 6 != 0:
            third = player_num//3+1
            if player_num % 6 < 3:
                third += 1
        else:
            third = player_num//3


        first_group = df_ranking.iloc[:third]
        second_group = df_ranking.iloc[third:-third]
        third_group = df_ranking.iloc[-third:]

        team_num = len(first_group)

        shuffled_first_group = first_group.sample(frac=1)
        shuffled_second_group = second_group.sample(frac=1)
        shuffled_third_group = third_group.sample(frac=1)

        teams = []
        for team_i in range(team_num):
            team = []
            team.append(_get_row_id(shuffled_first_group.iloc[[team_i]]))
            if team_i < len(shuffled_second_group):
                team.append(_get_row_id(shuffled_second_group.iloc[[team_i]]))
            else:
                team.append(TournamentData.SUB)
            team.append(_get_row_id(shuffled_third_group.iloc[[team_i]]))
            teams.append(team)
        
        return teams

    def _get_new_games(self, df_teams, round_num):
        teams = df_teams.loc[df_teams["ROUND_NUM"] == round_num]
        teams = teams.index
        if len(teams) % 2 != 0:
            raise Exception(f"Team number must be even: {len(teams)}")
        games = []
        for team1, team2 in zip(teams[:len(teams)//2], teams[-len(teams)//2:]):
            games.append([int(team1), int(team2)])
        return games

        

def _get_row_id(row):
    return row.index[0]
