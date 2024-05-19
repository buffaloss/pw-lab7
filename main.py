from json import load, dumps
from datetime import timedelta
from dotenv import dotenv_values
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint

config = dotenv_values()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = config['JWT_SECRET']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

app.register_blueprint(
    get_swaggerui_blueprint(
        '/api/swagger',
        '/static/swagger.yml',
        config={
            'app_name': "Locations API"
        }
    )
)

@app.route('/api/token/', methods=['POST'])
def token():
    data = request.get_json()
    if data['username'] == config['USERNAME'] and data['password'] == config['PASSWORD']:
        refresh_token = create_refresh_token(identity=data['permissions'])
        access_token = create_access_token(identity=data['permissions'])
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({'msg': 'Bad username or password'}), 401


@app.route('/api/refresh/', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200


@app.route('/api/location/<string:id>', methods=['GET'])
@jwt_required()
def location(id):
    try:
        permissions = get_jwt_identity()
        if 'G' in permissions:
            with open('locations.json', 'r') as file:
                locations = load(file)
            if id in locations:
                return jsonify({id: locations[id]}), 200
            else:
                return jsonify({'msg': 'Not found'}), 404
        else:
            return jsonify({'msg': 'Unauthorized'}), 403

    except:
        return jsonify({'msg': 'Internal server error'}), 500


@app.route('/api/location/', methods=['GET'])
@jwt_required()
def locations():
    try:
        permissions = get_jwt_identity()
        if 'G' in permissions:
            with open('locations.json', 'r') as file:
                locations = load(file)
            
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

            else:
                return jsonify(locations), 200
        else:
            return jsonify({'msg': 'Unauthorized'}), 403

    except:
        return jsonify({'msg': 'Internal server error'}), 500


@app.route('/api/location/', methods=['POST'])
@jwt_required()
def add_location():
    try:
        permissions = get_jwt_identity()
        if 'P' in permissions:
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
        else:
            return jsonify({'msg': 'Unauthorized'}), 403

    except:
        return jsonify({'msg': 'Internal server error'}), 500


@app.route('/api/location/', methods=['PUT'])
@jwt_required()
def update_location():
    try:
        permissions = get_jwt_identity()
        if 'U' in permissions:
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
        else:
            return jsonify({'msg': 'Unauthorized'}), 403

    except:
        return jsonify({'msg': 'Internal server error'}), 500


@app.route('/api/location/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_location(id):
    try:
        permissions = get_jwt_identity()
        if 'D' in permissions:
            with open('locations.json', 'r') as file:
                locations = load(file)
            if id not in locations:
                return jsonify({'msg': 'Not found'}), 404
            locations.pop(id)
            with open('locations.json', 'w') as file:
                file.write(dumps(locations, indent=4))
            return jsonify({'msg': 'Deleted'}), 200
        else:
            return jsonify({'msg': 'Unauthorized'}), 403

    except:
        return jsonify({'msg': 'Internal server error'}), 500


try:
    open('locations.json')
except FileNotFoundError:
    with open('locations.json', 'w') as file:
        file.write('{}')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
