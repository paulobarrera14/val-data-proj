import psycopg2

def connect_to_db():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="val_db",
        user="postgres",
        password="Chicharito14!!@"
    )

def drop_and_create_tables(connection):
    cursor = connection.cursor()

    # Drop existing tables if they exist
    tables_to_drop = ["matchInfo", "players"]  # You can add other table names here if needed
    for table in tables_to_drop:
        cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")

    # Create new tables based on the provided schema
    create_match_info = """
        CREATE TABLE matchInfo (
        match_id UUID PRIMARY KEY, -- Assuming UUID format for matchId
        map_id TEXT,
        game_version TEXT,
        game_length_millis BIGINT, -- Given that it's a millisecond value, it could be large
        region VARCHAR(10), -- 'eu' is short, but might want to leave room for other regions
        game_start_millis BIGINT, -- Same rationale as game_length_millis
        provisioning_flow_id TEXT,
        is_completed BOOLEAN,
        custom_game_name TEXT,
        queue_id TEXT,
        game_mode TEXT,
        is_ranked BOOLEAN,
        season_id UUID -- Assuming UUID format for seasonId
    );
    """

    create_player = """
        CREATE TABLE players (
        puuid TEXT PRIMARY KEY,
        game_name TEXT,
        tag_line VARCHAR(10),
        team_id TEXT,
        party_id UUID,
        character_id UUID,
        score INTEGER,
        rounds_played INTEGER,
        kills INTEGER,
        deaths INTEGER,
        assists INTEGER,
        playtime_millis BIGINT,
        grenade_casts INTEGER,
        ability1_casts INTEGER,
        ability2_casts INTEGER,
        ultimate_casts INTEGER,
        competitive_tier INTEGER,
        is_observer BOOLEAN,
        player_card UUID,
        player_title UUID
    );
    """

    cursor.execute(create_match_info)
    cursor.execute(create_player)

    connection.commit()
    cursor.close()

def main():
    conn = connect_to_db()
    drop_and_create_tables(conn)
    conn.close()

if __name__ == "__main__":
    main()