from flask import Blueprint, request, jsonify,current_app
import numpy as np
from validation.predict_validation import validate_input


predict_api = Blueprint('predict_api', __name__,url_prefix='/api')

@predict_api.route('/predict', methods=['POST'])
def get_predictions():
    try:
        data = request.json
        validate_input(data)
        model = current_app.config['model']
        data = data['data']
        turbidity = data['turbidity']
        ph = data['ph']
        conductivity = data['conductivity']
        min_alum = -1
        min_output = -1
        all_output = []
        for alum in range(6,14):
            np_input = np.array([ph,turbidity,conductivity,alum]).reshape(1, -1)
            prediction = model.predict(np_input)
            all_output.append(prediction[0])
            if prediction[0] < 5:
                if min_alum == -1:
                    min_alum = alum
                    min_output = prediction[0]
                elif prediction[0] < min_output:
                    min_alum = alum
                    min_output = prediction[0]
        return jsonify(
            {'prediction': min_alum,'output': min_output,'all_output': all_output}), 200
    except ValueError as e:
        print(e)
        return jsonify({'error': 'Invalid input'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'Unexpected Error Occured'}), 500
    


@predict_api.route('/send_readings',methods=['POST'])
def save_readings():
    try:
        data = request.json
        validate_input(data)
        ph = data['ph']
        turbidity = data['turbidity']
        conductivity = data['conductivity']
        alum = data['alum']
        sensor_id = data['sensor_id']
        mongo_db = current_app.config['mongo_db']
        collection = mongo_db['readings']
        collection.update_one({
            'sensor_id': sensor_id
        },{
            '$set': {
            'ph': ph,
            'turbidity': turbidity,
            'conductivity': conductivity,
            }
        },upsert=True)

        return jsonify({'message': 'Readings Saved'}), 200

       
    except ValueError as e:
        print(e)
        return jsonify({'error': 'Invalid input'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'Unexpected Error Occured'}), 500
    
@predict_api.route('/get_readings',methods=['GET'])
def get_readings():
    try:
        sensor_id = request.args.get('sensor_id')
        mongo_db = current_app.config['mongo_db']
        collection = mongo_db['readings']
        readings = collection.find_one({
            'sensor_id': sensor_id
        })
        if readings:
            return jsonify({'readings': readings}), 200
        else:
            return jsonify({'error': 'No readings found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Unexpected Error Occured'}), 500
    
@predict_api.route('/add_sensor',methods=['POST'])
def add_sensor():
    try:
        data = request.json
        sensor_id = data['sensor_id']
        mongo_db = current_app.config['mongo_db']
        collection = mongo_db['readings']
        collection.insert_one({
            'sensor_id': sensor_id,
            'ph': 0,
            'turbidity': 0,
            'conductivity': 0
        })
        return jsonify({'message': 'Sensor Added'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Unexpected Error Occured'}), 500
    