 📞 Twilio + Vapi Real-Time Conference Monitor

This project integrates **Twilio Programmable Voice** with **Vapi.ai** to enable browser-based voice conference calls with real-time audio monitoring via WebSocket.

---

## 📚 Table of Contents

- [📦 Prerequisites](#-prerequisites)
- [⚙️ Setup Guide](#️-setup-guide)
  - [🔐 How to Get Twilio Credentials](#-how-to-get-twilio-credentials)
  - [🔐 How to Get Vapi Credentials](#-how-to-get-vapi-credentials)
  - [🔧 Twilio Console Configuration](#-twilio-console-configuration)
  - [🔧 Vapi Dashboard Configuration](#-vapi-dashboard-configuration)
- [📂 Project Structure](#-project-structure)
- [🚀 Running the Project](#-running-the-project)
- [🛠️ Application Flow](#️-application-flow)
- [🧩 API Endpoints](#-api-endpoints)
- [🔒 Security Notes](#-security-notes)
- [✅ Next Steps](#-next-steps)

---

## 📦 Prerequisites

- Twilio Account [Sign up here](https://www.twilio.com/try-twilio)
- Vapi.ai Account [Sign up here](https://vapi.ai/)
- Basic understanding of:
  - Flask (Python)
  - Next.js (React)
  - WebSockets

---

## ⚙️ Setup Guide

### 🔐 How to Get Twilio Credentials

1. Log in to [Twilio Console](https://www.twilio.com/console)
2. Navigate to **Account > General Settings**
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
3. Navigate to **Programmable Voice > Tools > API Keys**
   - Create a new API Key to get:
     - `TWILIO_API_KEY_SID`
     - `TWILIO_API_KEY_SECRET`
4. Navigate to **Programmable Voice > Voice Settings**
   - Create a **Twilio Application SID** to get:
     - `TWIML_APP_SID`
5. Navigate to **Phone Numbers > Manage > Active Numbers**
   - Get a verified Twilio phone number:
     - `TWILIO_NUMBER`

---

### 🔐 How to Get Vapi Credentials

1. Log in to your [Vapi Dashboard](https://dashboard.vapi.ai/)
2. Create or use an existing assistant.
   - Get the `VAPI_ASSISTANT_ID`
3. Go to **API Keys** in the dashboard.
   - Create a new API key to get:
     - `VAPI_API_KEY`

---

### 🔧 Twilio Console Configuration

1. Go to **Twilio > Programmable Voice > TwiML Apps**  
   - Create a new TwiML App:
     - Voice URL: `https://your-backend-domain.com/api/conference` (for production)
     - For local development, use a tool like [ngrok](https://ngrok.com/) to expose your Flask server.

2. Save the **TwiML App SID** and set it as `TWIML_APP_SID` in your environment variables.

3. Configure the **Voice > Call Status Callback URL** to point to:
https://your-backend-domain.com/api/call-status


---

### 🔧 Vapi Dashboard Configuration

1. Go to your Assistant settings and enable:
- ✅ **Passive Listening (Monitor Mode)**
- ✅ **WebSocket Streaming (if configurable)**
2. Ensure the assistant can accept external call monitoring via API.

---

## 📂 Project Structure

project-root/
│
├── backend/ # Flask API
│ ├── app.py
│ └── requirements.txt
│
├── frontend/ # Next.js App Router
│ ├── app/
│ │ └── page.tsx
│ └── package.json
│
└── README.md

Copy
Edit

---

## 🔐 Environment Variables

Create a `.env` file in the backend directory:

```bash
## Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_API_KEY_SID=your_twilio_api_key_sid
TWILIO_API_KEY_SECRET=your_twilio_api_key_secret
TWIML_APP_SID=your_twiml_app_sid
TWILIO_NUMBER=your_twilio_phone_number

# Vapi Configuration
VAPI_API_KEY=your_vapi_api_key
VAPI_ASSISTANT_ID=your_vapi_assistant_id
```
## 🚀 Running the 

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🛠️ Application Flow
1. Token Generation
Browser requests Twilio Voice token from /api/token.

2. Call Initiation
Browser connects to Twilio conference via /api/conference (optionally calling an external number).

3. Conference Status Tracking
Twilio calls /api/call-status to track active CallSid for Vapi.

4. Vapi Monitoring
Browser requests /api/vapi_listen to get a Vapi WebSocket listen URL.

5. Real-Time Listening
Browser connects to Vapi WebSocket and passively listens to the audio in the conference.

## 🧩 API Endpoints
Endpoint	            Method	            Description
/api/token	            GET	                Generate Twilio access token
/api/conference	        POST	            Create/join Twilio conference
/api/call-status	    POST	            Twilio webhook for call tracking
/api/vapi_listen	    POST	            Initiate Vapi passive listening