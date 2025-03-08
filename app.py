from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import crontab
import os

DELAY = 120
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/adjust', methods=['GET'])
def adjust():
    action = request.args.get('action')
    duration = request.args.get('duration', type=int, default=5)  # New duration input
    if action == 'stop':
        cmd = 'pkill -f /root/blinds/run.py'
        os.system(cmd)
    elif action == 'reset':
        duration = DELAY
    print(f"Button pressed: {action}, Duration: {duration} seconds")  # Logging for debugging
    cmd = f'python /root/blinds/run.py {action} {duration}'
    os.system(cmd)
    return jsonify({"status": "success", "action": action, "duration": duration})


@app.route('/submit', methods=['GET'])
def submit():
    hours = request.args.get('hours', type=int, default=0)
    minutes = request.args.get('minutes', type=int, default=0)
    action = request.args.get('action', type=str, default='set')
    # Convert CST to GMT (CST is UTC-6, GMT is UTC+0)
    hours = hours+6
    print(f"Submitted: {hours} hours, {minutes} minutes -> GMT Time:")
    # Update cron job for blinds_down at GMT time
    cron = crontab.CronTab(user=True)
    cmd = f'python /root/blinds/run.py down {DELAY}'
    cron.remove_all(command=cmd)
    if action!='pause':
        job = cron.new(command=cmd, comment='blinds_down')
        job.setall(f"{minute} {hour} * * 1-5")
        cron.write()
    cmd = f'python /root/blinds/run.py reset {DELAY}'
    cron.remove_all(command=cmd)
    if action!='pause':
        job = cron.new(command=cmd, comment='blinds_reset')
        job.setall(f"{minute} {hour+2} * * 1-5")
        cron.write()
    return jsonify({"status": "success", "action": action, "gmt_hours": hour, "gmt_minutes": minute})

if __name__ == '__main__':
    app.run(debug=True)
