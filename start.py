from os import system, name
import subprocess
import json
import os

# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def create_config():
    if os.path.exists('config.json'):
        try: 
            os.remove('config.json')
        except OSError as e:
            print('Error deleting config file', e)
    
    config = {
        "jellyfin_url": input('Enter Jellyfin URL: '),
        "api_key": input('Enter API key: '),
        "user_id": input('Enter user ID: ')
    }

    with open('config.json', 'w') as f:
        json.dump(config, f)

    print('Config file defined.')
    clear()

def select_tool(tool):
    if tool == '1':
        print("\nRunning Duplicate Finder...")
        clear()
        subprocess.call(['python', 'tools/duplicate_finder.py'])
    elif tool == '2':
        print("\nRunning Missing Metadata Checker...")
        clear()
        subprocess.call(['python', 'tools/simple_metadata_check.py'])
    elif tool == '3':
        print("\nRunning Video Quality Identifier...")
        clear()
        subprocess.call(['python', 'tools/video_quality_identifier.py'])
    elif tool == '4':
        print("\nDefine config file...")
        if os.path.exists('config.json'):
            print('ERROR: Config file already exists!\n')
            reconfig = input('Reconfigure? (y/n) ')
            if reconfig == 'y':
                create_config()
                clear()
        else: 
            create_config()
            clear()
    else:
        print("Invalid tool number, please try again.")
        main()

def main():
    print("\nSelect a tool to use:")
    print("1. Duplicate Finder")
    print("2. Missing Metadata Checker")
    print("3. Video Quality Identifier")
    print("4. Define config file")
    print("5. Exit")
    tool = input("\nEnter the number of the tool: ")
    if tool == '5':
        print('\nbye :)')
        exit()
    select_tool(tool)

if __name__ == "__main__":
    clear()
    main()