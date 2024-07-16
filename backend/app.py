from flask import Flask, jsonify
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId


app = Flask(__name__)

def convert_objectid(doc):
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

@app.route('/api/show/<type>', methods=['GET'])
def show(type):
    if type == 'head':
        # retrieve first 5 documents
        documents = collection.find().limit(5)
    elif type == 'tail':
        # retrieve last 5 documents
        documents = collection.find().sort([('$natural', -1)]).limit(5)
    else:
        return 'Unsupported Type, Use \'head\' or \'tail\' types only!'
    # convert documents to json
    json_output = [convert_objectid(doc) for doc in documents]
    return jsonify(json_output)

def mongo_connect():
    try:
        client = MongoClient('mongodb://mongo-service:27017')
        print(f"Available databases: {client.list_database_names()}")
        db = client.churn_predictions
        collection = db.csv_data
        print(f"Collections in churn_predictions: {db.list_collection_names()}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    else:
        return client, db, collection


client, db, collection = mongo_connect()

@app.route('/api/<customer_id>', methods=['GET'])
def customer_by_id(customer_id):
    user = collection.find_one({"customerID": customer_id})

    if user:
        user.pop('_id')
        return jsonify(user)
    else:
        return jsonify({"error": f"User ID {customer_id} not found"}), 404

@app.route('/api/upload', methods=['POST'])
def upload_csv():
    df = pd.read_csv('data.csv')
    data = df.to_dict(orient='records')
    result = collection.insert_many(data)
    return jsonify({'result': 'Data inserted successfully', 'inserted_ids': str(result.inserted_ids)}), 201

@app.route('/api/all_data', methods=['GET'])
def get_all_data():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data), 200

@app.route('/api/charges/<monthly_charges>', methods=['GET'])
def submit_by_charges(monthly_charges):
    # Query MongoDB for customers with MonthlyCharges above the specified amount
    customers = collection.find({"MonthlyCharges": {"$gt": float(monthly_charges)}}).limit(15)
    customer_ids = [str(customer["customerID"]) for customer in customers]

    if customer_ids:
        return jsonify(customer_ids)
    else:
        return jsonify({"error": f"No customers found with MonthlyCharges above {monthly_charges}"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5005)
