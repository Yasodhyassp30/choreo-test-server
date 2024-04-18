from flask import Flask, request, jsonify,current_app
import os
import jwt 

def jwt_middleware():
    headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } 
    if request.method == 'OPTIONS' or request.method == 'options': return jsonify(headers), 200
    excluded_routes = ['/api/login', '/api/register','/api/send_readings']
    if request.path not in excluded_routes:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid JWT token"}), 401

        token = auth_header.split(' ')[1]
        try:
            key = current_app.config['SECRET_KEY']
            payload  = jwt.decode(token, key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Expired JWT token"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid JWT token"}), 401