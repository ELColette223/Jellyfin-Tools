import subprocess
import requests
import json
import os

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'start.py'))

def tryanother(url_jellyfin, api_key, user_id):
    tryanother = input("\nSearch in another category? (y or n) ")
    
    if tryanother == 'y':
        check_metadata(url_jellyfin, api_key, user_id)
    else:
        sure = input('Are you sure you want to exit? (press enter to exit) ')
        if sure == '':
            print('\nback to start.py...', )
            subprocess.call(['python', script_path])
            exit()
        else:
            pass

def get_user_input():
    try:
        with open('config.json') as f:
            config = json.load(f)
            url_jellyfin = config['jellyfin_url']
            api_key = config['api_key']
            user_id = config['user_id']
    except FileNotFoundError as e:
        print("Config file not found, please define it first.")
        print("Run start.py and select option 4.")
        print("Exiting...")
        exit()

    return url_jellyfin, api_key, user_id

def validate_url(url_jellyfin):
    try: 
        url_test = requests.get(url_jellyfin, timeout=10) 
        url_test.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print("\nSomething went wrong with the URL:", e)
        return False

def check_metadata(url_jellyfin, api_key, user_id):
    headers = {'X-Emby-Token': api_key,}

    # Request to get categories
    get_categories = requests.get(f"{url_jellyfin}/Users/{user_id}/Items", headers=headers, timeout=10)
    
    if get_categories.status_code == 200:
        categories = get_categories.json()['Items']
        print('\nAvailable categories:')
        category_dict = {}
        for i, category in enumerate(categories, start=1):
            print(f"{i}- ID: {category['Id']} - Name: {category['Name']}")
            category_dict[i] = category['Id']

        try:
            category_number = input("\nEnter the number of the Jellyfin Category (type 'exit' to exit): ")
            if category_number == 'exit':
                print('\nback to start.py...')
                subprocess.call(['python', script_path])
                exit()

            category_number = int(category_number)
            category_id = category_dict.get(category_number)

            if not category_id:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid category number.")
            check_metadata(url_jellyfin, api_key, user_id)
        
        # Request to get movies in the selected category
        response = requests.get(f"{url_jellyfin}/Users/{user_id}/Items?ParentId={category_id}&IncludeItemTypes=Movie", headers=headers)

        if response.status_code == 200:
            print("Searching for duplicates...")
            movies = response.json()
            movie_names = []
            duplicate_movies = []

            for item in movies['Items']:
                movie_name = item['Name']
                if movie_name in movie_names:
                    duplicate_movies.append(movie_name)
                else:
                    movie_names.append(movie_name)
            
            if len(duplicate_movies) > 0:
                print("\nDuplicates found!")
                for movie in duplicate_movies:
                    print("* ", movie)
                tryanother(url_jellyfin, api_key, user_id)

            else:
                print("\nNo duplicates found!")
                tryanother(url_jellyfin, api_key, user_id)
        else:
            print("\nError accessing Jellyfin API, error: ", response.status_code)
            if response.status_code == 401:
                print("Probably error in your API key")
            tryanother(url_jellyfin, api_key, user_id)
    else:
        print("\nError getting categories, error: ", get_categories.status_code)
        print("Check your API key!")
        tryanother(url_jellyfin, api_key, user_id)

def main():
    url_jellyfin, api_key, user_id = get_user_input()
    while not validate_url(url_jellyfin):
        print("\nPlease enter a valid Jellyfin URL.")
        url_jellyfin, api_key, user_id = get_user_input()

    check_metadata(url_jellyfin, api_key, user_id)

if __name__ == "__main__":
    main()