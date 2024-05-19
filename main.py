from json import load, dumps
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/location/<string:id>', methods=['GET'])
def location(id):
    try:
        with open('locations.json', 'r') as file:
            locations = load(file.read())
        if id in locations:
            return jsonify(locations[id]), 200
        else:
            return jsonify({'msg': 'Not found'}), 404

    except:
        return jsonify({'msg': 'Internal server error'}), 500


@app.route('/api/location', methods=['GET'])
def locations():
    try:
        with open('locations.json', 'r') as file:
            locations = load(file.read())
        
        if request.args.get('from'):
            from_id = int(request.args.get('from'))
            if request.args.get('count'):
                count = int(request.args.get('count'))
                for i in range(count):
                    if str(from_id + i) not in locations:
                        return jsonify({'msg': 'Not found'}), 404
                response = {}
                for i in range(count):
                    response[str(from_id + i)] = locations[str(from_id + i)]
                return jsonify(response), 200

    except:
        return jsonify({'msg': 'Internal server error'}), 500


@app.route('/api/location', methods=['POST'])
def add_location():
    try:
        with open('locations.json', 'r') as file:
            locations = load(file)
        data = request.get_json()
        for key in data.keys():
            if "name" not in data[key] or "description" not in data[key] or "rating" not in data[key] or "favourite" not in data[key] or len(data[key]) != 4:
                return jsonify({'msg': 'Bad request'}), 400
            if key in locations.keys():
                return jsonify({'msg': 'Conflict'}), 409
            locations[key] = data[key]
        with open('locations.json', 'w') as file:
            file.write(dumps(locations, indent=4))
        return jsonify({'msg': 'Created'}), 201

    except:
        return jsonify({'msg': 'Internal server error'}), 500


@app.route('/api/location', methods=['PUT'])
def update_location():
    try:
        with open('locations.json', 'r') as file:
            locations = load(file)
        data = request.get_json()
        id = list(data.keys())[0]
        if id not in locations:
            return jsonify({'msg': 'Not found'}), 404
        if "name" not in data[id] or "description" not in data[id] or "rating" not in data[id] or "favourite" not in data[id] or len(data[id]) != 4:
            return jsonify({'msg': 'Bad request'}), 400
        locations[id] = data
        with open('locations.json', 'w') as file:
            file.write(dumps(locations, indent=4))
        return jsonify({'msg': 'Updated'}), 200

    except:
        return jsonify({'msg': 'Internal server error'}), 500


@app.route('/api/location/<string:id>', methods=['DELETE'])
def delete_location(id):
    try:
        with open('locations.json', 'r') as file:
            locations = load(file)
        if id not in locations:
            return jsonify({'msg': 'Not found'}), 404
        locations.pop(id)
        with open('locations.json', 'w') as file:
            file.write(dumps(locations, indent=4))
        return jsonify({'msg': 'Deleted'}), 200

    except:
        return jsonify({'msg': 'Internal server error'}), 500


try:
    open('locations.json')
except FileNotFoundError:
    with open('locations.json', 'w') as file:
        file.write('{}')


app.run(host='0.0.0.0', port=5000)
