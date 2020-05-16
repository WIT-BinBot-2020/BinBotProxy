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
    timeRangeDays = request.args.get('rangeDays')
    timeRangeHours = request.args.get('rangeHours')
    timeRangeMinutes = request.args.get('rangeMinutes')

    if timeRangeDays is None:
        timeRangeDays = 1
    if timeRangeHours is None:
        timeRangeHours = 0
    if timeRangeMinutes is None:
        timeRangeMinutes = 0

    if not str(timeRangeDays).isnumeric():
        timeRangeDays = 1
    if not str(timeRangeHours).isnumeric():
        timeRangeHours = 0
    if not str(timeRangeMinutes).isnumeric():
        timeRangeMinutes = 0

    command = 'SELECT cpu, disk, ram FROM piSystemUsage WHERE time > now() - ' + str(timeRangeDays) + 'd - ' \
              + str(timeRangeHours) + 'h - ' + str(timeRangeMinutes) + 'm'

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


@app.route('/micKeyword')
def micKeyword():
       pass

@app.route('/micAngleArrival')
def micAngleArrival():
    timeRangeDays = request.args.get('rangeDays')
    timeRangeHours = request.args.get('rangeHours')
    timeRangeMinutes = request.args.get('rangeMinutes')

    if timeRangeDays is None:
        timeRangeDays = 1
    if timeRangeHours is None:
        timeRangeHours = 0
    if timeRangeMinutes is None:
        timeRangeMinutes = 0

    if not str(timeRangeDays).isnumeric():
        timeRangeDays = 1
    if not str(timeRangeHours).isnumeric():
        timeRangeHours = 0
    if not str(timeRangeMinutes).isnumeric():
        timeRangeMinutes = 0

    command = 'SELECT mic_direction_of_arrival from micAngleArrival WHERE time > now() - ' + str(timeRangeDays) + 'd - ' \
              + str(timeRangeHours) + 'h - ' + str(timeRangeMinutes) + 'm'
    print(command)
    data = db.query(command)
    for items in data:
        dataPoint = {
            "angles": items
        }
        return make_response(jsonify(dataPoint))

    return "Empty List"


@app.route('/commandFrequency')
def commandFrequency():

    command = 'SELECT distinct(command) from commands'
    data = db.query(command)
    commandData = []
    for items in data:
        for item in items:
            command = "SELECT COUNT(command) from commands where command = '" + item["distinct"] + "'"
            counts = db.query(command)
            for count in counts:
                thisCount = {
                    "Command": item["distinct"],
                    "Count" : count[0]["count"]
                }
                commandData.append(thisCount)

    return make_response(jsonify(commandData))


if __name__ == '__main__':
        app.run(host="0.0.0.0",debug=True)
