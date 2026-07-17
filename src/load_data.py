from pathlib import Path
import csv
import sqlite3


# Find the main project folder
project_folder = Path(__file__).resolve().parents[1]

# File locations
database_path = project_folder / "database" / "cases.db"
sql_file_path = project_folder / "sql" / "create_tables.sql"
csv_file_path = project_folder / "data" / "specialists.csv"


def create_database():
    """Create the SQLite tables using the SQL file."""

    # Create the database folder if it does not exist
    database_path.parent.mkdir(exist_ok=True)

    # Read the SQL commands
    sql_commands = sql_file_path.read_text(encoding="utf-8")

    # Connect to SQLite
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(sql_commands)

    print("Database tables created successfully.")


def load_specialists():
    """Read specialists.csv and insert its data into SQLite."""

    with csv_file_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        specialists = list(reader)

    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        for specialist in specialists:
            connection.execute(
                """
                INSERT OR REPLACE INTO specialists (
                    specialist_id,
                    name,
                    department
                )
                VALUES (?, ?, ?)
                """,
                (
                    int(specialist["specialist_id"]),
                    specialist["name"],
                    specialist["department"],
                ),
            )

        connection.commit()

    print(f"{len(specialists)} specialists were added.")


def display_specialists():
    """Display the specialist records stored in SQLite."""

    with sqlite3.connect(database_path) as connection:
        records = connection.execute(
            """
            SELECT specialist_id, name, department
            FROM specialists
            ORDER BY specialist_id
            """
        ).fetchall()

    print("\nSpecialists stored in the database:")

    for specialist_id, name, department in records:
        print(specialist_id, name, department)


def main():
    try:
        create_database()
        load_specialists()
        display_specialists()

    except FileNotFoundError as error:
        print("A required file could not be found:")
        print(error)

    except sqlite3.Error as error:
        print("A database error occurred:")
        print(error)


if __name__ == "__main__":
    main()
