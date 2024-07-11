from datetime import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd



app = Flask(__name__)


client = MongoClient('mongo-service', 27017)  
db = client.customer_db
collection = db.customers


@app.route('/')
def hello_world():
    return 'flask front is running'


@app.route('/flask/getTime', methods=['Get'])
def get_time():
    now = datetime.now()
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return f'The current time is: {current_time_str}'


@app.route('/flask/kinan', methods=['Get'])
def get_kinan():
    return f'The current time is: kinan'



@app.route('/flask/add', methods=['POST'])
def add_data():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'result': str(result.inserted_id)}), 201

@app.route('/upload', methods=['POST'])
def upload_csv():
    df = pd.read_csv('data.csv')

    data = df.to_dict(orient='records')
    result = collection.insert_many(data)
    return jsonify({'result': 'Data inserted successfully', 'inserted_ids': str(result.inserted_ids)}), 201

@app.route('/data', methods=['GET'])
def get_data():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, port=5005)
