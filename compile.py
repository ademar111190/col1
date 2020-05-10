#!/usr/bin/python3

from pathlib import Path
from sys import exit

SETTINGS_CONFIG_FILE="settings.config"

def read_setting():
    setting_file = Path(SETTINGS_CONFIG_FILE)
    if setting_file.is_file():
        settings = {}
        with open(SETTINGS_CONFIG_FILE) as f:
            lines = [line.rstrip() for line in f]
            for line in lines:
                key,value = line.split("=")
                settings[key] = value
        return settings
    else:
        return None

def main():
    settings = read_setting()
    if (settings is None):
        exit(f"Please create your {SETTINGS_CONFIG_FILE} as described in the README.md")
    print(settings)

if __name__ == "__main__":
    main()
