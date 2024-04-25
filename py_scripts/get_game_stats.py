import csv
import json
import requests
from random import randrange
from tabulate import tabulate


# Stats to get
key_general = ["GamesPlayed"]
key_attack_stats = ["EfgPct", "Fg3Pct", "FtPoints", "FTA", "Turnovers", "TotalPoss"]
key_defend_stats = ["Steals", "Blocks", "Fouls"]
key_all_stats = key_general + key_attack_stats + key_defend_stats

# Uitil functions
def get_team_players(game_stats, team_type):
    team = []
    if team_type == "Away":
        stats = game_stats["Away"]["FullGame"]
    elif team_type == "Home":
        stats = game_stats["Home"]["FullGame"]

    for entity in stats:
        if entity["Name"] != "Team":
            team.append([entity["Name"], entity["Minutes"]])
    team.sort(key=lambda lst: lst[1], reverse=True)
    return team


def get_player_ids(game_type, team, team_type):
    if team_type == "Away":
        team_id = game_overview["AwayTeamId"]
    elif team_type == "Home":
        team_id = game_overview["HomeTeamId"]

    players_url = "https://api.pbpstats.com/get-team-players-for-season"
    players_params = {
        "Season": game_season,
        "SeasonType": game_type,
        "TeamId": team_id
    }
    players_response = requests.get(players_url, params=players_params)
    players = players_response.json()["players"]

    # "team" is list of list, each sub list starts with player name
    for player in team:
        for id, name in players.items():
            if name == player[0]:
                player.append(id)

def get_player_stats_by_id(id, game_season, game_type):
    url = "https://api.pbpstats.com/get-all-season-stats/nba"
    params = {
        "EntityType": "Player",
        "EntityId": id
    }
    player_stats = requests.get(url, params=params).json()

    for json_object in player_stats["results"][game_type]:
        for key, value in json_object.items():
            if key == "Season" and value == game_season:
                return json_object


def get_team_stats(team, game_season, game_type):
    for player in team:
        all_stats = get_player_stats_by_id(player[2], game_season, game_type)
        for key in key_all_stats:
            if key in all_stats:
                player.append(all_stats[key])
            else:
                player.append(None)
        # Add player position
        # player.append(get_player_position(player[2]))

def get_player_position(player_id):
    from nba_api.stats.endpoints import commonplayerinfo
    player_info = commonplayerinfo.CommonPlayerInfo(player_id)
    player_info = player_info.get_normalized_dict()
    # Map the position to 5 short terms: PG, SG, SF, PF, C
    position_map = {
        "" : "PG", # Default to "PG"
        "Guard": "PG",
        "Point-Guard": "PG",
        "Shooting-Guard": "SG",
        "Forward-Guard": "SG",
        "Forward": "SF",
        "Guard-Forward": "SF",
        "Small-Forward": "SF",
        "Power-Forward": "PF",
        "Center-Forward": "PF",
        "Center": "C",
        "Forward-Center": "C",
    }
    return position_map[player_info["CommonPlayerInfo"][0]["POSITION"]]

# Print messages
def print_table(team):
    col_names = ["Name", "Minutes", "ID"] + key_all_stats
    print(tabulate(team, headers=col_names, tablefmt="grid"))

def get_game_stats(game_id=None):
    if game_id is None:
        # Year range
        start_year = 2010
        end_year = 2020
        year = randrange(start_year, end_year)
        game_season = str(year) + "-" + str((year + 1) % 100).rjust(2, "0")

        # Game type
        game_types = ["Regular Season", "Playoffs"]
        game_type = game_types[randrange(len(game_types))]

        # Game data
        players_url = "https://api.pbpstats.com/get-games/nba"
        games_params = {
            "Season": game_season,
            "SeasonType": game_type
        }
        response = requests.get(players_url, params=games_params)
        response_json = response.json()["results"]

        # Random a game
        game_id = randrange(len(response_json))
        game_overview = response_json[game_id]
        game_id = game_overview["GameId"]
        print(json.dumps(game_overview, indent=2))

    print("Extracting game stats for game:", game_overview["GameId"], "...")
    players_url = "https://api.pbpstats.com/get-game-stats"
    games_params = {
        "GameId": game_overview["GameId"],
        "Type": "Player" # options are Player, Lineup and LineupOpponent
    }
    response = requests.get(players_url, params=games_params)
    game_stats = response.json()['stats']
    return game_season, game_type, game_overview, game_stats

def export_origin_game_results(game_overview):
    # Export the game result to the CSV file
    orig_results_file = "data/game_origin_results.csv"

    with open(orig_results_file, "r") as file:
        reader = csv.reader(file)
        # Check if the file is empty
        if len(file.read()) == 0:
            print("Empty file, Writing the header to the file")
            with open(orig_results_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["game_id", 
                                "home_id", 
                                "away_id", 
                                "home_abbr", 
                                "away_abbr", 
                                "home_points", 
                                "away_points"])

        # Check if the game is already in the file by the game ID
        is_game_in_file = False
        for row in reader:
            if row[0] == game_overview["GameId"]:
                print("The game is already in the file")
                is_game_in_file = True
                break
        
        if not is_game_in_file:
            print("Writing the game result to the file")
            with open(orig_results_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([game_overview["GameId"],
                                game_overview["HomeTeamId"],
                                game_overview["AwayTeamId"],
                                game_overview["HomeTeamAbbreviation"],
                                game_overview["AwayTeamAbbreviation"],
                                game_overview["HomePoints"],
                                game_overview["AwayPoints"]])

# Export the lineup players key stats
def export_lineup(game_season, game_type, game_stats, is_home):
    team_type = "Home" if is_home else "Away"
    team_stats = get_team_players(game_stats, team_type)
    get_player_ids(game_type, team_stats, team_type)
    get_team_stats(team_stats, game_season, game_type)
    col_names = ["Name", "Minutes", "ID"] + key_all_stats
    team_stats = [{col_names[i]: player[i] for i in range(len(col_names))} for player in team_stats]
    
    for player in team_stats:
        player["Position"] = get_player_position(player["ID"])
        # Calculate the PassRatio
        # If Turnovers or TotalPoss is None, then use the average value of the team
        if player["Turnovers"] is None or player["TotalPoss"] is None:
            team_turnovers = [player["Turnovers"] for player in team_stats if player["Turnovers"] is not None]
            team_total_poss = [player["TotalPoss"] for player in team_stats if player["TotalPoss"] is not None]
            player["Turnovers"] = sum(team_turnovers) / len(team_turnovers)
            player["TotalPoss"] = sum(team_total_poss) / len(team_total_poss)
        player["PassRatio"] = 1 - player["Turnovers"] / player["TotalPoss"]

    print(tabulate(team_stats[:], headers="keys", tablefmt="grid"))

    positions = ["PG", "SG", "SF", "PF", "C"]
    lineup = {}
    lineup_ids = []
    for position in positions:
        lineup[position] = None
    for player in team_stats:
        if lineup[player["Position"]] is None and player["Position"] in positions:
            lineup[player["Position"]] = player
            lineup_ids.append(player["ID"])

    for position in lineup:
        if lineup[position] is None:
            for player in team_stats:
                if player['ID'] not in lineup_ids:
                    lineup[position] = player
                    lineup_ids.append(player["ID"])
                    break

    print(f"The lineup of the {team_type} team:")
    for position in lineup:
        print(position + ":", lineup[position])

    # Export the lineup to a CSV file
    # The columns include position, PassRatio, Fg2Pct, ID, name
    LINEUP_FILE = f"data/lineup_{team_type.lower()}_{game_overview['GameId']}.csv"
    with open(LINEUP_FILE, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["Position", "PassRatio", "EfgPct", "ID", "Name"])
        for position in lineup:
            player = lineup[position]
            writer.writerow([position, player["PassRatio"], player["EfgPct"], player["ID"], player["Name"]])
    
    return lineup

def read_lineup(team_type, game_overview):
    # Read the lineup from the CSV file
    LINEUP_FILE = f"data/lineup_{team_type.lower()}_{game_overview['GameId']}.csv"
    with open(LINEUP_FILE, mode="r") as file:
        reader = csv.reader(file)
        lineup = []
        for i, row in enumerate(reader):
            if i == 0:
                continue
            if row:
                lineup.append(row)
    return lineup

def generate_pcsp_lineup(team_type, game_overview):
    # Generate the PCSP lineup stats for the game base on the template file "game_template.pcsp"
    # Replace the first lines of the below code with the lineup stats
    lineup = read_lineup(team_type, game_overview)
    positions = ["PG", "SG", "SF", "PF", "C"]
    stats = ""
    for position in positions:
        for player in lineup:
            if player[0] == position:
                stats += f"#define player{position}Pass {int(float(player[1]) * 100)};\n"
                stats += f"#define player{position}Score {int(float(player[2]) * 100)};\n"

    PCSP_DIR = "pcsp_files"
    PCSP_TEMPLATE = "game_template.pcsp"
    PCSP_FILE = f"{PCSP_DIR}/game_{game_overview['GameId']}_{team_type.lower()}.pcsp"
    
    with open(PCSP_TEMPLATE, mode="r") as file:
        template = file.read()
    with open(PCSP_FILE, mode="w") as file:
        # Replace the first 10 lines of the template with the lineup stats
        # Remove the first 10 lines of the template
        template = template.split("\n")[10:]
        file.write(stats)
        file.write("\n")
        file.write("\n".join(template))

if __name__ == "__main__":
    game_season, game_type, game_overview, game_stats = get_game_stats()

    # Export the game result to the CSV file
    export_origin_game_results(game_overview)
    
    # Export the lineup stats
    export_lineup(game_season, game_type, game_stats, is_home=True)
    export_lineup(game_season, game_type, game_stats, is_home=False)
    
    # Generate the PCSP lineup stats
    generate_pcsp_lineup("Home", game_overview)
    generate_pcsp_lineup("Away", game_overview)