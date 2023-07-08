import requests
import urllib
from .loading import Loading


access_key = input('Please input unsplash key, or here the key in the unsplash.py file: ')

class Unsplash:
    def save_image(query, path):
        loading = Loading('Finding cover image')

        params = {'query': query, 'per_page': 1}

        headers = {'Accept-Version': 'v1', 'Authorization': f'Client-ID {access_key}'}

        response = requests.get('https://api.unsplash.com/search/photos', params=params, headers=headers)
        
        if response.status_code == 200:
            photo_url = response.json()['results'][0]['urls']['regular']
            urllib.request.urlretrieve(photo_url, path)
        else:
            print('Error:', response.status_code)

        loading.complete()