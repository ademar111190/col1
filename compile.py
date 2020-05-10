#!/usr/bin/python3

from pathlib import Path
from sys import exit
from sqlite3 import connect


SETTINGS_CONFIG_FILE="settings.config"


def read_setting():
    setting_file = Path(SETTINGS_CONFIG_FILE)
    if setting_file.is_file():
        settings = {}
        with open(SETTINGS_CONFIG_FILE) as f:
            lines = [line.rstrip() for line in f]
            for line in lines:
                key,value = line.split("=")
                settings[key] = value.replace("\\", "")
        return settings
    else:
        return None


def connect_compiled_db(settings):
    compiled_db_file = Path(settings["compiledDb"])
    db_exists = compiled_db_file.is_file()
    connection = connect(compiled_db_file)
    cursor = connection.cursor()
    if not db_exists:
        cursor.execute("CREATE TABLE IF NOT EXISTS user(email TEXT, pass TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS fileRead(name TEXT)")
        connection.commit()
    return connection


def get_collection1_files(settings):
    return list(Path(settings["collection1"]).rglob("*.[tT][xX][tT]"))


def read_collection1_file_content(compiled_db, file):
    cursor = compiled_db.cursor()
    cursor.execute(f"SELECT COUNT(1) FROM fileRead WHERE name=\"{file}\";")
    file_has_been_read = int(cursor.fetchone()[0]) > 0
    print(file_has_been_read)
    if file_has_been_read:
        return None
    else:
        return []


def write_collection1_file_content(compiled_db, file, data):
    cursor = compiled_db.cursor()
    cursor.execute(f"INSERT INTO fileRead VALUES (\"{file}\");")
    compiled_db.commit()


def main():
    settings = read_setting()
    if (settings is None):
        exit(f"Please create your {SETTINGS_CONFIG_FILE} as described in the README.md")
    compiled_db = connect_compiled_db(settings)
    collection1_files = get_collection1_files(settings)
    print(len(collection1_files))
    for f in collection1_files:
        data = read_collection1_file_content(compiled_db, f)
        if data is not None:
            write_collection1_file_content(compiled_db, f, data)
    compiled_db.close()


if __name__ == "__main__":
    main()
