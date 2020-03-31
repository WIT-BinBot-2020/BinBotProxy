from flask import Flask, jsonify, make_response
from flask_cors import CORS
from influxdb import InfluxDBClient
import json

def createApp():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app

def connectInflux():
    client = InfluxDBClient(host='localhost', port=8086, database='BinBotStats')
    return client

app = createApp()
db = connectInflux()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/piStats')
def piStats():
    command = 'SELECT cpu, disk, ram from piSystemUsage'
    data = db.query(command)
    usageData = []
    for items in data:
        for item in items:
            dataPoint = {
                "time": item["time"],
                "cpu": item["cpu"],
                "disk": item["disk"],
                "ram": item["ram"],
            }
            usageData.append(dataPoint)

    return make_response(jsonify(usageData))

@app.route('/batLevel')
def batLevel():
    command = 'SELECT level from batLevel ORDER BY DESC LIMIT 1'
    data = db.query(command)
    for items in data:
        return make_response(jsonify(items[0]))

    return "Error"


if __name__ == '__main__':
        app.run(host="0.0.0.0",debug=True)
