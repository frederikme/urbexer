'''
Example of how you can make api calls to the server
'''
import requests
from PIL import Image
from io import BytesIO

BASE_URL = 'http://127.0.0.1:5000'

# This request fetches all ID's of urbexlocations that are located in that boundingbox
# example usage, let's just take our entire planet
data = {
    'west': -90,
    'east': 90,
    'south': -90,
    'north': 90
}
r = requests.post(f'{BASE_URL}/discover', json=data)
ids = r.json().get('locations')
print(f"Locations that meet the requirements to be in the bounding box have the ids \nof {ids}")

# Iterate through each of the locations ids
for id in ids:
    location = requests.get(f'{BASE_URL}/location/{id}').json()

    # parse data of each location
    print('name:', location.get('name'))
    print('lat', location.get('latitude'), 'lon', location.get('longitude'))
    #print('description:', location.get('description'))
    print('\n')

    # get all stored images for that location
    images = requests.get(f'{BASE_URL}/location/images/{id}').json().get('images')
    print(f"images stored for this location \nare {images}")

    for image in images:
        r = requests.get(f'{BASE_URL}/location/images/{id}/{image}')
        i = Image.open(BytesIO(r.content))
        print('Opening and saving one of the images as proof of concept.')
        i.show()
        i.save('saved_image.jpg')
        print('Images saved as saved_image.jpg')
        print('Bye... :-)')
        exit()