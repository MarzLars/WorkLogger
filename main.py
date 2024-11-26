from flask import Flask, render_template, jsonify, request, send_file
from time_tracker import TimeTracker
import os
import csv

app = Flask(__name__)
tracker = TimeTracker()
csv_delimiter = ','

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
            reader = csv.reader(file, delimiter=csv_delimiter)
            for row in reader:
                if row[0] == f"sep={csv_delimiter}":
                    continue
                if row == ['Description', 'Date', 'Week', 'Time Spent', 'Hours', 'Minutes', 'Seconds']:
                    continue
                logs.append(row)
    return jsonify({'logs': logs})

# Route to set the CSV delimiter
@app.route('/set_delimiter', methods=['POST'])
def set_delimiter():
    global csv_delimiter
    csv_delimiter = request.json.get('delimiter', ',')
    return jsonify({'status': 'delimiter set'})

# Route to export the logs
@app.route('/export', methods=['GET'])
def export():
    if os.path.exists('time_log.csv'):
        return send_file('time_log.csv', as_attachment=True)
    else:
        return jsonify({'error': 'No logs to export'}), 404

if __name__ == "__main__":
    app.run(debug=True)