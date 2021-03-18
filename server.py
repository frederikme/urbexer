from flask import Flask
from flask import request, send_file, render_template
import json, os

app = Flask(__name__)
database = 'data.json'

@app.route('/', methods=['GET'])
def index():
    fp = open(database)
    jsondata = json.load(fp)

    data = []

    for key, value in jsondata.items():
        data.append([value.get('latitude'), value.get('longitude'), value.get('name'), value.get('description'), key])

    fp.close()

    return render_template('index.html', data=data)

@app.route('/discover', methods=['POST'])
def discover():
    keys = []

    if request.method == 'POST':
        form = request.json

        west, east, south, north = form.get('west'), form.get('east'), form.get('south'), form.get('north')

        fp = open(database)
        data = json.load(fp)

        for key, value in data.items():
            lat = value.get('latitude')
            lon = value.get('longitude')
            if lat > south and lat < north:
                if lon > west and lon < east:
                    keys.append(key)

        fp.close()

    return {"locations": keys}

@app.route('/location/<location_id>', methods=['GET'])
def location(location_id):
    if request.method == 'GET':
        fp = open(database)
        data = json.load(fp)
        location = data.get(location_id)
        fp.close()
        return location

@app.route('/location/images/<location_id>/<image>', methods=['GET'])
def image(location_id, image):
    if request.method == 'GET':
        return send_file(f'images/{location_id}/{image}')

@app.route('/location/images/<location_id>', methods=['GET'])
def location_images(location_id):
    names = []
    if request.method == 'GET':
        names = os.listdir(f'images/{location_id}')

    return {'images': names}

if __name__ == '__main__':
    app.run()
