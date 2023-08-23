import psycopg2
from psycopg2.extensions import AsIs


def connect_to_db():
    return psycopg2.connect(
        dbname="val_db",
        user="postgres",
        password="Chicharito14!!@",
        host="localhost",
        port="5432"
    )


def check_database_size(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
    size = cursor.fetchone()[0]
    cursor.close()
    return size

def get_record_counts(connection):
    cursor = connection.cursor()
    query = """
    SELECT 'matchinfo' AS table_name, COUNT(*) AS record_count FROM matchinfo
    UNION ALL
    SELECT 'players', COUNT(*) FROM players;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def get_top_players_by_unique_match_for_rank(connection, rank, limit=10):
    cursor = connection.cursor()
    query = """
    SELECT DISTINCT ON (game_name) game_name, p.score, p.match_id, p.rounds_played
    FROM players p
    JOIN matchinfo m ON p.match_id = m.match_id
    WHERE competitive_tier = %s
    ORDER BY game_name, p.match_id
    LIMIT %s;
    """
    cursor.execute(query, (rank, limit))
    results = cursor.fetchall()
    cursor.close()
    return results

if __name__ == "__main__":
    conn = connect_to_db()

    # Check entire database size
    db_size = check_database_size(conn)
    print(f"Size of the entire database: {db_size}")

    record_counts = get_record_counts(conn)
    for table_name, count in record_counts:
        print(f"Table '{table_name}' has {count} records.")

    rank = 9  # Change this to your desired rank
    players = get_top_players_by_unique_match_for_rank(conn, rank)

    print(f"Top {len(players)} players with rank {rank} from unique matches:")
    for player_name, score, match_id, rounds_played in players:
        avg_score = round(score / rounds_played)
        print(f"{player_name} (Match: {match_id}): {avg_score}")

conn.close()