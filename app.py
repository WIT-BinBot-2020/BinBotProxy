from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from influxdb import InfluxDBClient
import json

def createApp():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app

def connectInflux():
    client = InfluxDBClient(host='52.19.82.33', port=8086, database='BinBotStats', username='binbot', password='b33pb00p!!')
    return client

app = createApp()
db = connectInflux()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/piStats')
def piStats():
    timeRange = request.args.get('range')

    if timeRange is None:
        timeRange = 30

    if not timeRange.isnumeric():
        timeRange = 30

    command = 'SELECT cpu, disk, ram FROM piSystemUsage WHERE time > now() - ' + str(timeRange) + 'd'
    print(command)
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

@app.route('/recentMessages')
def recentMessages():
    command = 'SELECT message from messages ORDER BY DESC LIMIT 5'
    data = db.query(command)
    messageData = []
    for items in data:
        for item in items:
            dataPoint = {
                "message": item["message"]
            }
            messageData.append(dataPoint)

    return make_response(jsonify(messageData))


if __name__ == '__main__':
        app.run(host="0.0.0.0",debug=True)
