import requests

def search_unsplash(query):
    access_key = '3uN1NQ3pLdTTnDxIcvuBsMbqGCD00_BrC-tiuuVHf5g'
    base_url = 'https://api.unsplash.com/search/photos'
    
    params = {
        'query': query,
        'per_page': 1,  # Retrieve only one result
        'client_id': access_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad requests

        data = response.json()

        if 'results' in data and data['results']:
            result = data['results'][0]
            print("Best-Matched Image:")
            print(f"Image URL: {result['urls']['regular']}")
            print(f"Image Dimensions: {result['width']} x {result['height']}")
        else:
            print(f"No images found on Unsplash for the query: {query}")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except Exception as err:
        print(f"Error: {err}")

# Example usage
query = input("Enter your search query for images: ")
search_unsplash(query)
