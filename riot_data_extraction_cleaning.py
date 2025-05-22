import requests
import pandas as pd
import json
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
server = 'sea'

from google.colab import drive
drive.mount('/content/drive')

# Define the Riot API key
with open('/content/drive/MyDrive/Colab Notebooks/data/riot_api_key.txt', 'r') as file:
    key = file.read().strip()

# Create a session for making requests
session = requests.Session()

# Define function to fetch data from the Riot API
def fetch_data(api_url):
    response = session.get(api_url, headers={'X-Riot-Token': key})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from API. Status code: {response.status_code}")
        return None

# Fetch the latest version for static data
version_url = 'https://ddragon.leagueoflegends.com/api/versions.json'
versions = fetch_data(version_url)
latest_version = versions[0] if versions else 'latest'

# Fetch champion data
champion_url = f'http://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json'
champion_data = fetch_data(champion_url)

# Create a dictionary mapping champion IDs to champion names
champion_list = {int(data['key']): data['name'] for data in champion_data['data'].values()}

# Example list of tuples containing match ID, game name, blue team name, and red team name
match_list = [

    ("OC1_661825907", "Round 2 Match 1 Game 1", "QUTB", "AUEC"),
    ("OC1_661830971", "Round 2 Match 1 Game 2", "QUTB", "AUEC"),
    ("OC1_661828352", "Round 2 Match 2 Game 1", "QUTW", "MUE1"),
    ("OC1_661835084", "Round 2 Match 2 Game 2", "MUE1", "QUTW"),
    ("OC1_661829317", "Round 2 Match 3 Game 1", "UTSB", "UQ"),
    ("OC1_661833792", "Round 2 Match 3 Game 2", "UTSB", "UQ"),
    ("OC1_661839452", "Round 2 Match 3 Game 3", "UQ", "UTSB"),
    ("OC1_661828251", "Round 2 Match 4 Game 1", "SWIN", "UOC"),
    ("OC1_661830631", "Round 2 Match 4 Game 2", "SWIN", "UOC"),
    ("OC1_661834806", "Round 2 Match 4 Game 3", "UOC", "SWIN"),

    ("OC1_662538988", "Round 3 Match 1 Game 1", "UQ", "QUTB"),
    ("OC1_662546836", "Round 3 Match 1 Game 2", "QUTB", "UQ"),
    ("OC1_662541385", "Round 3 Match 2 Game 1", "MUE1", "SWIN"),
    ("OC1_662550387", "Round 3 Match 2 Game 2", "MUE1", "SWIN"),
    ("OC1_662557162", "Round 3 Match 2 Game 3", "MUE1", "SWIN"),
    ("OC1_662542009", "Round 3 Match 3 Game 1", "UTSB", "AUEC"),
    ("OC1_662543190", "Round 3 Match 4 Game 1", "UOC", "QUTW"),
    ("OC1_662548456", "Round 3 Match 4 Game 2", "QUTW", "UOC"),

    ("OC1_663392692", "Round 4 Match 1 Game 1", "UTSB", "QUTW"),
    ("OC1_663401368", "Round 4 Match 1 Game 2", "QUTW", "UTSB"),
    ("OC1_663410315", "Round 4 Match 1 Game 3", "UTSB", "QUTW"),
    ("OC1_663395590", "Round 4 Match 2 Game 1", "MUE1", "UQ"),
    ("OC1_663401688", "Round 4 Match 2 Game 2", "MUE1", "UQ"),
    ("OC1_663394647", "Round 4 Match 3 Game 1", "UOC", "QUTB"),
    ("OC1_663403494", "Round 4 Match 3 Game 2", "UOC", "QUTB"),
    ("OC1_663408509", "Round 4 Match 3 Game 3", "UOC", "QUTB"),

    ("OC1_665013828", "Round 5 Match 1 Game 1", "UTSB", "UQ"),
    ("OC1_665020406", "Round 5 Match 1 Game 2", "UTSB", "UQ"),
    ("OC1_665014518", "Round 5 Match 2 Game 1", "QUTW", "QUTB"),
    ("OC1_665020754", "Round 5 Match 2 Game 2", "QUTB", "QUTW"),
    ("OC1_665016366", "Round 5 Match 3 Game 1", "UOC", "SWIN"),
    ("OC1_665023516", "Round 5 Match 3 Game 2", "UOC", "SWIN"),

    ("OC1_665748251", "Round 6 Match 1 Game 1", "UTSB", "QUTB"),
    ("OC1_665750918", "Round 6 Match 1 Game 2", "UTSB", "QUTB"),
    ("OC1_665746261", "Round 6 Match 2 Game 0", "QUTW", "UQ"),
    ("OC1_665747670", "Round 6 Match 2 Game 1", "QUTW", "UQ"),
    ("OC1_665750985", "Round 6 Match 2 Game 2", "UQ", "QUTW"),
]

# Initialize an empty list to store player data
player_data_list = []

# Define function to calculate KS
def calculate_ks(participant_kills, total_team_kills):
    if total_team_kills != 0:
        return participant_kills / total_team_kills
    else:
        return 0

# Define function to calculate D%
def calculate_d_percent(participant_deaths, total_team_deaths):
    if total_team_deaths != 0:
        return participant_deaths / total_team_deaths
    else:
        return 0

# Loop through each match tuple and fetch data for all players in the match
for match_id, game_name, blue_team_name, red_team_name in match_list:
    api_url = f'https://{server}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={key}'
    match_data = fetch_data(api_url)

    if match_data:
        game_duration_minutes = match_data['info']['gameDuration'] / 60
        game_duration_display = match_data['info']['gameDuration'] / (60*60*24)

        # Extracting bans for both teams with specific ban order
        ban_order = {100: [1, 3, 5, 8, 10], 200: [2, 4, 6, 7, 9]}
        bans = {100: [], 200: []}
        for team in match_data['info']['teams']:
            team_id = team['teamId']
            for i, ban in enumerate(team['bans']):
                champion_name = champion_list.get(ban['championId'], 'Unknown')
                bans[team_id].append(f"{champion_name}{ban_order[team_id][i]}")

        # Assign bans to individual players
        ban_indices = {100: 0, 200: 0}  # Track the next ban index for each team

        # Extract total kills and deaths for each team
        team_kills = {100: 0, 200: 0}
        team_deaths = {100: 0, 200: 0}
        for participant in match_data['info']['participants']:
            team_id = participant['teamId']
            team_kills[team_id] += participant.get('kills', 0)
            team_deaths[team_id] += participant.get('deaths', 0)

        # Loop through each participant again to calculate KS and D%
        for participant in match_data['info']['participants']:
            team_id = participant['teamId']
            team_win = next((team['win'] for team in match_data['info']['teams'] if team['teamId'] == team_id), False)
            team_gold_earned = sum([p['goldEarned'] for p in match_data['info']['participants'] if p['teamId'] == team_id])
            role = participant['individualPosition']
            participant_kills = participant.get('kills', 0)
            participant_deaths = participant.get('deaths', 0)

            # Calculate KS and D%
            ks = calculate_ks(participant_kills, team_kills[team_id])
            d_percent = calculate_d_percent(participant_deaths, team_deaths[team_id])

            # Extracting First Blood data
            first_blood_assist = participant.get('firstBloodAssist', False)
            first_blood_kill = participant.get('firstBloodKill', False)
            FBPAR = 1 if first_blood_assist or first_blood_kill else 0

            # Assign the next ban in order
            ban = bans[team_id][ban_indices[team_id]] if ban_indices[team_id] < len(bans[team_id]) else 'No Ban'
            ban_indices[team_id] += 1

            player_info = {
                'Summoner Name': participant['riotIdGameName']+"#"+participant['riotIdTagline'],
                'Role': role,
                'Champion': participant['championName'],
                'Ban': ban,  # Assign individual ban to player
                'K': participant.get('kills', 0),
                'D': participant.get('deaths', 0),
                'A': participant.get('assists', 0),
                'KDA': participant['challenges'].get('kda', 0),
                'KPAR': participant['challenges'].get('killParticipation', -1),
                'KS': ks,
                'D%': d_percent,
                'CS(Minion)': participant.get('totalMinionsKilled', 0),
                'CS(JG camps)': participant.get('neutralMinionsKilled', 0),
                'Total CS': participant.get('totalMinionsKilled', 0) + participant.get('neutralMinionsKilled', 0),
                'CS@10': participant['challenges'].get('laneMinionsFirst10Minutes', 0) + participant['challenges'].get('jungleCsBefore10Minutes', 0),
                'CS/M': (participant.get('totalMinionsKilled', 0) + participant.get('neutralMinionsKilled', 0)) / game_duration_minutes if game_duration_minutes != 0 else 0,
                'G': participant['goldEarned'],
                'G/M': participant['challenges'].get('goldPerMinute', 0),
                'GS': participant['goldEarned'] / team_gold_earned if team_gold_earned != 0 else 0,
                'DMG': participant.get('totalDamageDealtToChampions', 0),
                'DMG/M': participant.get('totalDamageDealtToChampions', 0) / game_duration_minutes if game_duration_minutes != 0 else 0,
                'DMG%': participant['challenges'].get('teamDamagePercentage', 0),
                'DMG/GOLD': participant.get('totalDamageDealtToChampions', 0) / participant.get('goldEarned', 1) if participant.get('goldEarned', 0) != 0 else 0,
                'DT': participant.get('totalDamageTaken', 0),
                'DT/D': participant.get('totalDamageTaken', 0) / (participant.get('deaths', 1) if participant.get('deaths', 0) != 0 else 1),
                'DT%': participant['challenges'].get('damageTakenOnTeamPercentage', 0),
                'WARD/M': participant.get('wardsPlaced', 0) / game_duration_minutes if game_duration_minutes != 0 else 0,
                'SWEEP/M': participant.get('wardsKilled', 0) / game_duration_minutes if game_duration_minutes != 0 else 0,
                'Vision Score/M': participant['challenges'].get('visionScorePerMinute', 0),
                'FBPAR': FBPAR,
                'Win/Lose': 'Win' if team_win else 'Lose',
                'Side': 'Blue' if team_id == 100 else 'Red',
                'Game Time': game_duration_display,
                'Patch': match_data['info']['gameVersion'],
                'Game Name': game_name,  # Include game name
                'Team Name': blue_team_name if team_id == 100 else red_team_name  # Assign the correct team name based on side
            }

            player_data_list.append(player_info)

# Convert the list to a dataframe
player_df = pd.DataFrame(player_data_list)

# Display the dataframe
player_df

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/content/drive/MyDrive/Colab Notebooks/data/credentials.json', scope)
client = gspread.authorize(credentials)

# Open the existing Google Sheet by its ID
sheet_id = '1wZmUYCck06KxDRpXexnkKp_WzmJndTIab7W9nC3MJJY'
sheet = client.open_by_key(sheet_id)

# Select the first worksheet
worksheet = sheet.get_worksheet(0)

# Convert the DataFrame to a list of lists
data = player_df.values.tolist()

# Get the column names from the DataFrame
column_names = player_df.columns.tolist()

# Insert the column names into the first row of the data
data.insert(0, column_names)

# Clear the existing content in the worksheet
worksheet.clear()

# Insert the data into the worksheet starting from cell A1
worksheet.update('A1', data)

print("Data successfully exported to Google Sheet.")
