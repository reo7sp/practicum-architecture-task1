#!/usr/bin/env python3
import os
import random
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

LOCATION_TO_SENSOR_ID = {
    'Living Room': '1',
    'Bedroom': '2',
    'Kitchen': '3'
}

SENSOR_ID_TO_LOCATION = {
    '1': 'Living Room',
    '2': 'Bedroom',
    '3': 'Kitchen'
}


def get_sensor_id_from_location(location):
    return LOCATION_TO_SENSOR_ID.get(location, '0')


def get_location_from_sensor_id(sensor_id):
    return SENSOR_ID_TO_LOCATION.get(sensor_id, 'Unknown')


def generate_random_temperature():
    return round(random.uniform(18.0, 25.0), 2)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/temperature', methods=['GET'])
def get_temperature():
    location = request.args.get('location', '')
    sensor_id = request.args.get('sensorId', '')

    if not location:
        location = get_location_from_sensor_id(sensor_id)

    if not sensor_id:
        sensor_id = get_sensor_id_from_location(location)

    temperature_value = generate_random_temperature()

    response = {
        'value': temperature_value,
        'unit': 'Celsius',
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'location': location,
        'status': 'active',
        'sensor_id': sensor_id,
        'sensor_type': 'temperature',
        'description': f'Temperature sensor reading for {location}'
    }

    return jsonify(response), 200


@app.route('/temperature/<sensor_id>', methods=['GET'])
def get_temperature_by_id(sensor_id):
    location = get_location_from_sensor_id(sensor_id)

    temperature_value = generate_random_temperature()

    response = {
        'value': temperature_value,
        'unit': 'Celsius',
        'timestamp': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'location': location,
        'status': 'active',
        'sensor_id': sensor_id,
        'sensor_type': 'temperature',
        'description': f'Temperature sensor reading for {location}'
    }

    return jsonify(response), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)
