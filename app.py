from flask import Flask, jsonify, make_response
from flask_cors import CORS
from influxdb import InfluxDBClient
import json

def createApp():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app

def connectInflux():
    client = InfluxDBClient(host='34.246.184.109', port=8086, database='BinBotStats')
    return client

app = createApp()
db = connectInflux()

if __name__ == '__main__':
    app.run(debug=True)


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