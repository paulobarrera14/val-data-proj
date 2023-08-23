import psycopg2
import json
import os


def connect_to_db():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="val_db",
        user="postgres",
        password="Chicharito14!!@"
    )


def insert_match_info(cursor, data):
    query = """
        INSERT INTO matchInfo(
            match_id, map_id, game_version, game_length_millis, region, 
            game_start_millis, provisioning_flow_id, is_completed, custom_game_name, 
            queue_id, game_mode, is_ranked, season_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

    try:
        match_info = data['matchInfo']

        # Print the match_info to debug
        print(match_info)

        cursor.execute(query, (
            match_info['matchId'],
            match_info['mapId'],
            match_info['gameVersion'],
            match_info.get('gameLengthMillis', 0),
            match_info['region'],
            match_info['gameStartMillis'],
            match_info['provisioningFlowId'],
            match_info['isCompleted'],
            match_info['customGameName'],
            match_info['queueId'],
            match_info['gameMode'],
            match_info['isRanked'],
            match_info['seasonId']
        ))
    except KeyError as e:
        print(f"Error: {e} not found in data. Skipping...")

def insert_players(cursor, data):
    query = """
            INSERT INTO players (
                puuid, match_id, game_name, tag_line, team_id, party_id, 
                character_id, score, rounds_played, kills, deaths, assists, 
                playtime_millis, grenade_casts, ability1_casts, ability2_casts, 
                ultimate_casts, competitive_tier, is_observer, player_card, player_title
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (puuid) DO NOTHING;
            """

    match_id = data['matchInfo']['matchId']
    for player_data in data['players']:
        print(player_data)
        stats = player_data.get('stats') or {}
        abilityCasts = stats.get('abilityCasts') or {}

        cursor.execute(query, (
            player_data.get('puuid'), match_id, player_data.get('gameName'),
            player_data.get('tagLine'), player_data.get('teamId'),
            player_data.get('partyId'), player_data.get('characterId'),
            stats.get('score'), stats.get('roundsPlayed'),
            stats.get('kills'), stats.get('deaths'), stats.get('assists'),
            stats.get('playtimeMillis'), abilityCasts.get('grenadeCasts'),
            abilityCasts.get('ability1Casts'), abilityCasts.get('ability2Casts'),
            abilityCasts.get('ultimateCasts'), player_data.get('competitiveTier'),
            player_data.get('isObserver'), player_data.get('playerCard'),
            player_data.get('playerTitle')
        ))

def process_file(cursor, file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        # Insert match information and players
        insert_match_info(cursor, data)
        insert_players(cursor, data)

def main():
    conn = connect_to_db()
    cursor = conn.cursor()

    folder_path = "C:/Users/paulo/Desktop/Database/sample_data"
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            process_file(cursor, os.path.join(folder_path, filename))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()