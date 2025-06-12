from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.rest import Client
import os
import requests

app = Flask(__name__)
CORS(app)

# Twilio Configuration
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
API_KEY_SID = os.getenv("TWILIO_API_KEY_SID")
API_KEY_SECRET = os.getenv("TWILIO_API_KEY_SECRET")
TWIML_APP_SID = os.getenv("TWIML_APP_SID")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

# Vapi Configuration
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

client = Client(ACCOUNT_SID, AUTH_TOKEN)
CONFERENCE_NAME = 'MyConferenceRoom'
active_call_sid = None  # Track the active browser call

# ✅ Token Endpoint
@app.route('/api/token', methods=['GET'])
def token():
    identity = request.args.get('identity', 'web_user')
    token = AccessToken(ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET, identity=identity)
    voice_grant = VoiceGrant(outgoing_application_sid=TWIML_APP_SID, incoming_allow=True)
    token.add_grant(voice_grant)
    return jsonify({'token': token.to_jwt(), 'identity': identity})


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working!'})

# ✅ Conference Webhook
@app.route('/api/conference', methods=['POST'])
def conference():
    to_number = request.form.get('To')
    response = VoiceResponse()
    dial = Dial()
    dial.conference(
        CONFERENCE_NAME,
        start_conference_on_enter=True,
        end_conference_on_exit=True,
        status_callback="/api/call-status",
        status_callback_event="join leave start end",
        status_callback_method="POST"
    )
    response.append(dial)

    # Call external number and add to conference
    if to_number:
        client.calls.create(
            to=to_number,
            from_=TWILIO_NUMBER,
            twiml=f'<Response><Dial><Conference>{CONFERENCE_NAME}</Conference></Dial></Response>'
        )

    return Response(str(response), mimetype='text/xml')


# ✅ Twilio Call Status Webhook
@app.route('/api/call-status', methods=['POST'])
def call_status():
    global active_call_sid
    active_call_sid = request.form.get('CallSid')  # Save CallSid to use for Vapi
    print(f"Call status event received. Active CallSid: {active_call_sid}")
    return ('', 204)


# ✅ Vapi Listen Endpoint
@app.route('/api/vapi_listen', methods=['POST'])
def vapi_listen():
    if not active_call_sid:
        return jsonify({'error': 'No active call SID'}), 400

    vapi_response = requests.post(
        "https://api.vapi.ai/call",
        headers={
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "assistantId": VAPI_ASSISTANT_ID,
            "callSid": active_call_sid,
            "monitor": {"listen": True}
        }
    )

    if vapi_response.status_code != 200:
        return jsonify({'error': 'Vapi listen request failed'}), 500

    vapi_data = vapi_response.json()
    listen_url = vapi_data.get('monitor', {}).get('listenUrl')

    if not listen_url:
        return jsonify({'error': 'No listen URL provided by Vapi'}), 500

    return jsonify({'listenUrl': listen_url})


if __name__ == '__main__':
    app.run(debug=True)
