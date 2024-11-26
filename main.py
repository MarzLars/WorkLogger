from flask import Flask, render_template, jsonify, request
from time_tracker import TimeTracker
import os
import csv

app = Flask(__name__)
tracker = TimeTracker()

# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to start the time tracker
@app.route('/start', methods=['POST'])
def start():
    tracker.start()
    return jsonify({'status': 'started'})

# Route to pause the time tracker
@app.route('/pause', methods=['POST'])
def pause():
    tracker.pause()
    return jsonify({'status': 'paused'})

# Route to stop the time tracker and log the time
@app.route('/stop', methods=['POST'])
def stop():
    tracker.stop()
    description = request.json.get('description', '')
    tracker.log_time(description)
    return jsonify({'status': 'stopped'})

# Route to get the elapsed time
@app.route('/elapsed_time', methods=['GET'])
def elapsed_time():
    elapsed_time = tracker.get_elapsed_time()
    return jsonify({'elapsed_time': elapsed_time})

# Route to get the logs
@app.route('/logs', methods=['GET'])
def logs():
    logs = []
    if os.path.exists('time_log.csv'):
        with open('time_log.csv', mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if row[0] == "sep=;":
                    continue
                if row == ['Description', 'Date', 'Week', 'Time Spent', 'Hours', 'Minutes', 'Seconds']:
                    continue
                logs.append(row)
    return jsonify({'logs': logs})

if __name__ == "__main__":
    app.run(debug=True)