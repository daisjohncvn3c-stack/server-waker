import os
from flask import Flask, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Server Control</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #1a1a1a; color: white; margin: 0; }
        .card { text-align: center; background: #2a2a2a; padding: 40px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); width: 300px; }
        .btn { border: none; padding: 15px 25px; font-size: 16px; border-radius: 6px; cursor: pointer; color: white; width: 100%; margin-top: 15px; }
        .btn-wake { background: #007bff; }
        .btn-wake:hover { background: #0056b3; }
        .btn-start { background: #28a745; }
        .btn-start:hover { background: #1e7e34; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Minecraft Server</h2>
        <form action="/wake" method="post">
            <button type="submit" class="btn btn-wake">Wake Up Server</button>
        </form>
        <form action="/start" method="post">
            <button type="submit" class="btn btn-start">Turn On Server</button>
        </form>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


# Note the triple quotes (""") around the Cookie to allow multi-line strings
HEADERS = {
    "Authorization": "Bearer ptlc_bHDT3bkhF1x",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


@app.route("/wake", methods=["POST"])
def wake():
    wake_url = "https://panel.play.hosting/api/client/servers/5ba25eae-2f7d-44e8-9063-2e46800cad6a/wake"
    try:
        response = requests.post(wake_url, headers=HEADERS)
        if response.status_code in [200, 204]:
            return "<h3>Server is waking up! You can close this tab.</h3>"
        return f"<h3>Failed to wake server. Status: {response.status_code}</h3>"
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"


@app.route("/start", methods=["POST"])
def start():
    start_url = "https://panel.play.hosting/api/client/servers/5ba25eae-2f7d-44e8-9063-2e46800cad6a/power"
    try:
        response = requests.post(
            start_url, headers=HEADERS, json={"signal": "start"}
        )
        if response.status_code in [200, 204]:
            return "<h3>Server turning on! You can close this tab.</h3>"
        return f"<h3>Failed to start server. Status: {response.status_code}</h3>"
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
