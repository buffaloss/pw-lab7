from json import loads, dumps
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/location/<string:id>', methods=['GET'])
def location(id):
    try:
        with open('locations.json', 'r') as file:
            locations = loads(file.read())
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
            locations = loads(file.read())
        
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


try:
    open('locations.json')
except FileNotFoundError:
    with open('locations.json', 'w') as file:
        file.write('{}')


app.run(host='0.0.0.0', port=5000)
