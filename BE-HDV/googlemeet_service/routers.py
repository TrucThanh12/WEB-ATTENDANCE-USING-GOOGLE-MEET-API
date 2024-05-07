from flask import Flask, jsonify, request
from call_apis_meet import MeetAPI
import asyncio
import json
from worker import public
import time
app = Flask(__name__)
meet = MeetAPI()

@app.route('/api/googlemeet/get_participants', methods=['GET'])
def get_participants():
    public("(googlemeet-service) Start get participants:.....")
    start_time = time.time()
    meeting_id = request.args.get('meeting_id')
    participants = asyncio.run(meet.get_participants(meeting_id))
    print(participants)
    end_time = time.time()
    public("(googlemeet-service) End get participants time: {}...." + str(end_time - start_time))
    return jsonify(participants)

@app.route('/api/googlemeet/create_meet', methods=['POST'])
def create_meeting():
    response = asyncio.run(meet.create_space())
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)