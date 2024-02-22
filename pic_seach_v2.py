import requests

def custom_search(api_key, cx, query):
    base_url = "https://www.googleapis.com/customsearch/v1"

    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'searchType': 'image',
        'num': 1,
        'imgSize': 'xxlarge',  
       
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        data = response.json()
        best_match = get_best_match(data)
        display_best_match(best_match)

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except Exception as err:
        print(f"Error: {err}")

def get_best_match(data):
    items = data.get('items', [])
    return items[0] if items else None

def display_best_match(result):
    if not result:
        print("No best-matched image found.")
        return

    print("Best-Matched Image:")
    print(f"Image URL: {result.get('link', 'N/A')}")
    print(f"Image Dimensions: {result.get('image', {}).get('width', 'N/A')} x {result.get('image', {}).get('height', 'N/A')}")
    print(f"Image File Type: {result.get('mime', 'N/A')}")


api_key = 'AIzaSyB13Iv4E6Q-YmRtNmUT7oKvYPUbeqXfhEE'
cx = 'b78a0a9221f18477e'
query = input("Enter your base search query for website background images: ")
custom_search(api_key, cx, query)
