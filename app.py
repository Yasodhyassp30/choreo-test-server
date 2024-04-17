from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import os
import joblib
from pymongo import MongoClient
import certifi
from waitress import serve
import requests
import zipfile





app = Flask(__name__)
CORS(app)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')

model_path = 'models/model.pkl'

if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        model = joblib.load(f)
else:
    with zipfile.ZipFile('models/model.zip', 'r') as zip_ref:
        zip_ref.extractall('models')
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = joblib.load(f)
   
    else:
        print('Failed to download the model')



app.config['model'] = model

mongo_client = MongoClient(f"mongodb+srv://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}.mongodb.net/fyp?retryWrites={os.environ['MONGO_RETRY']}&w={os.environ['MONGO_PARAMS2']}",tlsCAFile=certifi.where())
mongo_db = mongo_client[app.config['MONGO_DBNAME']]

try:
    server_ping = mongo_client.admin.command('ping')
    if server_ping['ok']==1:
        print("Mongo Connected")
except:
    print("Mongo Not Connected")


 


if __name__ == '__main__':
    from apis.user_api import user_api
    from apis.predict_api import predict_api
    from middleware.token_validation import jwt_middleware
    import os
    import requests
    import joblib

    app.before_request(jwt_middleware)
    app.register_blueprint(predict_api)
    app.register_blueprint(user_api)
    serve(app, host='0.0.0.0', port=os.getenv('PORT'))
    