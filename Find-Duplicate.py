import requests

def tryanother():
    tryanother = input("\nTry another category? (y or n) ")
    
    if tryanother == 'y':
        start()
    else:
        print('\nbye :)')
        exit()

def start():
    url_jellyfin = input("\nEnter your Jellyfin URL (http://example:8096): ")
    api_key = input("\nEnter your Jellyfin API Key: ")
    user_id = input("\nEnter your Jellyfin User ID: ")

    headers = {'X-Emby-Token': api_key,}


    # Request to get categories
    get_categories = requests.get(f"{url_jellyfin}/Users/{user_id}/Items", headers=headers)
    
    if get_categories.status_code == 200:
        categories = get_categories.json()['Items']
        print('Available categories:')
        for category in categories:
            print(f"ID: {category['Id']} - Name: {category['Name']}")
        
        category_id = input("\nEnter the Jellyfin Category ID: ")  
        
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
                tryanother()

            else:
                print("\nNo duplicates found!")
                tryanother()

            print("\n")
        else:
            print("Error accessing Jellyfin API, error: ", response.status_code)
            if response.status_code == 401:
                print("Probably error in your API key")
    else:
        print("Error getting categories, error: ", get_categories.status_code)
        print("Check your API key!")

def main():
    start()

if __name__ == "__main__":
    main()