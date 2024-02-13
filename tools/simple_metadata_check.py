import requests
import concurrent.futures
import json
import os
import subprocess

CHECK_IMAGES = False
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'start.py'))

def tryanother(url_jellyfin, api_key, user_id):
    choice = input("\nTry another category? (y or n) ")
    
    if choice.lower() == 'y':
        check_metadata(url_jellyfin, api_key, user_id)
    else:
        sure = input('Are you sure you want to exit? (press enter to exit) ')
        if sure == '':
            print('\nback to start.py...', )
            subprocess.call(['python', script_path])
            exit()
        else:
            pass

def has_image(url_jellyfin, api_key, content_id):
    image_url = f"{url_jellyfin}/Items/{content_id}/Images/Primary"
    headers = {'X-Emby-Token': api_key,}
    response = requests.get(image_url, headers=headers, timeout=10)
    return response.status_code == 200

def metadata_check(url_jellyfin, api_key, item):
    required_metadata = ['Name', 'ProductionYear']
    has_required_metadata = all(key in item for key in required_metadata)
    if CHECK_IMAGES:
        return has_required_metadata and has_image(url_jellyfin, api_key, item['Id'])
    else:
        return has_required_metadata

def check_item(url_jellyfin, api_key, item):
    if not metadata_check(url_jellyfin, api_key, item):
        return item['Name']
    return None

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

    check_images_input = input('Do you want to check for images? (this option may cause issues, but is more precise) (y or n): ')
    global CHECK_IMAGES
    CHECK_IMAGES = check_images_input == 'y'
    return url_jellyfin, api_key, user_id

def validate_url(url_jellyfin):
    try: 
        url_test = requests.get(url_jellyfin, timeout=10) 
        url_test.raise_for_status()  # Raise an exception if the request was unsuccessful
        return True
    except requests.exceptions.RequestException as e:
        print("Something went wrong with the URL:", e)
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
        response = requests.get(f"{url_jellyfin}/Users/{user_id}/Items?ParentId={category_id}&IncludeItemTypes=Movie", headers=headers, timeout=10)

        if response.status_code == 200:
            print("Checking for missing metadata... (this may take a while)")
            movies = response.json()['Items']

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(check_item, url_jellyfin, api_key, item) for item in movies]
                missing_metadata = []
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        missing_metadata.append(result)
                    print('.', end='', flush=True)

            if missing_metadata:
                print("\nMovies with missing metadata:")
                for movie in missing_metadata:
                    print("* ", movie)
                tryanother(url_jellyfin, api_key, user_id)

            else:
                print("\nAll movies have basic metadata!")
                tryanother(url_jellyfin, api_key, user_id)

        else:
            print("Error accessing Jellyfin API, error: ", response.status_code)
            if response.status_code == 401:
                print("Probably error in your API key")
            main()
    else:
        print("Error getting categories, error: ", get_categories.status_code)
        print("Check your API key!")
        main()

def main():
    url_jellyfin, api_key, user_id = get_user_input()
    while not validate_url(url_jellyfin):
        print("\nPlease enter a valid Jellyfin URL.")
        url_jellyfin, api_key, user_id = get_user_input()

    check_metadata(url_jellyfin, api_key, user_id)

if __name__ == "__main__":
    main()
