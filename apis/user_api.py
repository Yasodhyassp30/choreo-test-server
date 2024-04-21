import datetime
import os
from flask import Blueprint,request,jsonify,current_app
import jwt
from validation.user_validation import validate_user,validate_login
import bcrypt
from app import mongo_db as db

user_api = Blueprint('user',__name__,url_prefix='/api')


@user_api.route('/register',methods=['POST'])
def register():
    try:
        user = request.json
        validate_user(user)
        

        user_exists = db.users.find_one({'email': user['email']})
        if user_exists:
            return jsonify({'error': 'User already exists'}), 400
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), salt)
        user['password'] = hashed_password

        result = db.users.insert_one(user)
        if result.inserted_id:
            del user['password']
            user['_id'] = str(result.inserted_id)
            payload = {
                'id': str(result.inserted_id),
                'email': user['email'],
                'exp': datetime.datetime.utcnow()+datetime.timedelta(days=1)
            }
            key = os.getenv('SECRET_KEY')
            token = jwt.encode(payload, key, algorithm='HS256')
            user['token'] = token
            return jsonify({'user':user,'message': 'User created successfully'}), 201
        else:
            return jsonify({'error':"Error"}),500
    except (ValueError, TypeError) as ve_te:
        return jsonify({'error': 'Invalid data format: ' + str(ve_te)}), 400
    except Exception as e:
        print(e)       
        return jsonify({'error': 'An unexpected error occurred'}), 500

@user_api.route('/login',methods=['POST'])
def login():
    try:
        user = request.json
        validate_login(user)
        user_exists = db.users.find_one({'email': user['email']})
        if user_exists:
            if bcrypt.checkpw(user['password'].encode('utf-8'), user_exists['password']):
                del user_exists['password']
                payload = {
                    'id': str(user_exists['_id']),
                    'email': user_exists['email'],
                    'exp': datetime.datetime.utcnow()+datetime.timedelta(days=1)
                }
                key = os.getenv('SECRET_KEY')
                token = jwt.encode(payload, key, algorithm='HS256')
                user_exists['token'] = token
                user_exists['_id'] = str(user_exists['_id'])
                return jsonify({'user':user_exists,'message': 'User logged in successfully'}), 200
            else:
                return jsonify({'error': 'Invalid credentials'}), 400
        else:
            return jsonify({'error': 'User not found'}), 404
    except (ValueError, TypeError) as ve_te:
        return jsonify({'error': 'Invalid data format: ' + str(ve_te)}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500
    

@user_api.route('/validate_token',methods=['GET'])
def is_valid():
    return jsonify({'message': 'Token is valid'}), 200