import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

# Configured via Render Environment Variables
API_KEY = os.environ.get("ptlc_SfwGdnatOeFIQc6R7nNvDkZvmXIwH4EkGVhHyDVucHm")
SERVER_ID = os.environ.get("SERVER_ID", "5ba25eae")
PANEL_URL = f"https://panel.play.hosting/api/client/servers/{SERVER_ID}/power"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Server Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #121212; color: white; margin: 0; }
        .card { text-align: center; background: #1e1e1e; padding: 30px; border-radius: 12px; width: 85%; max-width: 320px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .btn { border: none; padding: 15px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; color: white; width: 100%; margin-top: 15px; }
        .btn-start { background: #28a745; }
        .btn-stop { background: #dc3545; }
        .btn-restart { background: #ffc107; color: black; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Minecraft Server</h2>
        <form action="/power/start" method="post"><button type="submit" class="btn btn-start">Start / Wake</button></form>
        <form action="/power/restart" method="post"><button type="submit" class="btn btn-restart">Restart</button></form>
        <form action="/power/stop" method="post"><button type="submit" class="btn btn-stop">Stop</button></form>
    </div>
</body>
</html>
"""

def send_power_signal(signal):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"signal": signal}
    
    try:
        response = requests.post(PANEL_URL, json=payload, headers=headers, timeout=10)
        # Pterodactyl API returns 204 No Content on success
        return response.status_code in [200, 204]
    except Exception as e:
        print(f"Error sending request: {e}")
        return False

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/power/<signal>", methods=["POST"])
def handle_power(signal):
    if signal not in ["start", "stop", "restart", "kill"]:
        return "Invalid signal", 400
        
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"signal": signal}
    
    try:
        response = requests.post(PANEL_URL, json=payload, headers=headers, timeout=10)
        
        # Display exact response details if it fails
        if response.status_code in [200, 204]:
            return f"<h3>Successfully sent '{signal}' signal!</h3><a href='/'>Go Back</a>"
        else:
            return f"""
            <h3>Failed to send '{signal}' signal.</h3>
            <p><b>Status Code:</b> {response.status_code}</p>
            <p><b>Response Body:</b> {response.text}</p>
            <a href='/'>Go Back</a>
            """
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><a href='/'>Go Back</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
