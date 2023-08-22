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


if __name__ == "__main__":
    conn = connect_to_db()

    # Check entire database size
    db_size = check_database_size(conn)
    print(f"Size of the entire database: {db_size}")

    conn.close()