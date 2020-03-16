import random
import csv
import os

SUB = "SUB"

def init_players(player_keys):
    '''
    Initializes the player_list by the player_keys.
    '''
    player_list = []
    for key in player_keys:
        add_player(player_list, key)
    return player_list

def add_player(player_list, player_key):
    '''
    Adds a new player_key to the player_list.
    A new player is initialized by a dictionary of its key (or name) which must be unique,
    wins, ties, losses, played_games, goal_diff, and in_schedule boolean.
    '''
    if player_key in [player["name"] for player in player_list]:
        raise Exception("Player already exists!")
    player_list.append({"name": player_key,
                        "points": 0,
                        "wins": 0,
                        "ties": 0,
                        "loss": 0,
                        "played_games": 0,
                        "goal_diff": 0,
                        "in_schedule": True})


def remove_player(player_list, player_key):
    '''
    Removes a player by its key from the player_list.
    '''
    for i, player in enumerate(player_list):
        if player_key == player["name"]:
            del player_list[i]
            return

def find_player(player_list, player_key):
    for player in player_list:
        if player["name"] == player_key:
            return player
        if player_key == "SUB":
            return None
    raise Exception(f"Player {player_key} not found!")

def key_function(player):
    '''
    Key function for sorting/ranking the player list by points, goal difference and played games.
    '''
    return (player["points"], player["goal_diff"], -player["played_games"])
        
def rank_player_list(player_list):
    '''
    Sort the player_list of the dictionary by the key function.
    '''
    player_list.sort(key=key_function, reverse=True)

def update_member(member, goals_scored, goals_received):
    if member == None:
        return
    # WIN
    if goals_scored - goals_received > 0:
        member["wins"] += 1
        member["points"] += 3
    # TIE
    elif goals_scored - goals_received == 0:
        member["ties"] += 1
        member["points"] += 1
    # LOSS
    elif goals_scored - goals_received < 0:
        member["loss"] += 1
    member["played_games"] += 1
    member["goal_diff"] += goals_scored - goals_received

def update_schedule(games, round_number):
    for i, (team1, team2, result) in enumerate(games):
        for member in team1:
            update_member(member, goals_scored=result[0], goals_received=result[1])
        for member in team2:
            update_member(member, goals_scored=result[1], goals_received=result[0])

def get_new_teams(player_list):
    '''
    Generates new teams from the player list.
    First of all the player list is split up into three parts.
    The first part contains the probably better players.
    The second part contains the probably average players.
    The thrid part contains the probably worser players.
    Each team consists of the three sections, in which a good player,
    an average player and a bad player \"always\" play together.
    For this the number of players must always be divisible by 6,
    if this is not the case, SUBs are added to the second part.
    So the first and third part are always the same size.
    '''
    # Rank for fair divisions
    rank_player_list(player_list)
    ranked_player_list = player_list
    
    # Filter by in_schedule to give the players a break which are not in_schedule.
    in_schedule_player_list = []
    players_not_in_schedule = []

    for player in ranked_player_list:
        if player["in_schedule"]:
            in_schedule_player_list.append(player)
        else:
            players_not_in_schedule.append(player)
    
    num_players = len(in_schedule_player_list)
    if num_players % 6 != 0:
        third = num_players//3+1
        if num_players % 6 < 3:
            third += 1
    else:
        third = num_players//3
    first_third = in_schedule_player_list[0:third]
    last_third = in_schedule_player_list[-third:]
    center_third = in_schedule_player_list[third:-third]

    teams = []
    player1_list = list(range(0, len(first_third)))
    player2_list = list(range(0, len(center_third)))
    player3_list = list(range(0, len(last_third)))

    random.shuffle(player1_list)
    random.shuffle(player2_list)
    random.shuffle(player3_list)


    while len(player2_list) < len(player1_list):
        player2_list.append(None)

    teams = []
    for p1, p2, p3 in zip(player1_list, player2_list, player3_list):
        if p2 != None:
            teams.append([first_third[p1], center_third[p2], last_third[p3]])
        else:
            teams.append([first_third[p1], None, last_third[p3]])
    
    return teams, players_not_in_schedule

def get_new_round(teams):
    '''
    Generates a new round using the teams list.
    The teams list must be even.
    '''
    if len(teams) % 2 != 0:
        raise Exception(f"Team number must be even: {len(teams)}")
    games = []
    for team1, team2 in zip(teams[:len(teams)//2], teams[-len(teams)//2:]):
        games.append([team1, team2])
    return games


def save_ranking_list_to_csv(path, player_list, round_number):
    if not os.path.exists(path):
        os.mkdir(path)

    keys = player_list[0].keys()
    with open(f'{path}/ranking_list_round_{round_number}.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(player_list)

def load_ranking_list_from_csv(path, round_number):
    if not os.path.exists(path):
        os.mkdir(path)

    player_list = []
    with open(f'{path}/ranking_list_round_{round_number}.csv', 'r') as input_file:
        dict_reader = csv.DictReader(input_file)
        for player in dict_reader:
            for key in ["points","wins","ties","loss","played_games","goal_diff"]:
                player[key] = int(player[key])
            player_list.append(dict(player))
            
    return player_list

def save_round_games_to_csv(path, round_number, games):
    if not os.path.exists(path):
        os.mkdir(path)

    with open(f'{path}/round_games_{round_number}.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Player1Team1', 'Player2Team1', 'Player3Team1', 'Player1Team2', 'Player2Team2', 'Player3Team2', 'GoalsTeam1', 'GoalsTeam2'])
        for team1, team2, goals1, goals2 in games:
            writer.writerow([team1[0]["name"] if type(team1[0]) == dict else "SUB",
                             team1[1]["name"] if type(team1[1]) == dict else "SUB",
                             team1[2]["name"] if type(team1[2]) == dict else "SUB",
                             team2[0]["name"] if type(team2[0]) == dict else "SUB",
                             team2[1]["name"] if type(team2[1]) == dict else "SUB",
                             team2[2]["name"] if type(team2[2]) == dict else "SUB",
                             goals1,
                             goals2])

def load_round_games_from_csv(path, player_list, round_number):
    if not os.path.exists(path):
        os.mkdir(path)
    
    games = []
    results = []
    with open(f'{path}/round_games_{round_number}.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        for i, (team1p1, team1p2, team1p3, team2p1, team2p2, team2p3, goals1, goals2) in enumerate(reader):
            if i == 0:
                continue
            games.append([[find_player(player_list, team1p1), find_player(player_list, team1p2), find_player(player_list, team1p3)],
                          [find_player(player_list, team2p1), find_player(player_list, team2p2), find_player(player_list, team2p3)]])
            results.append([goals1,
                            goals2])

    return games, results
        