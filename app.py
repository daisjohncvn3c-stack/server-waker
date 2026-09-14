import os
from flask import Flask, render_template_string
from playwright.sync_api import sync_playwright

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

# Store credentials safely (or replace directly with your panel login info)
PANEL_LOGIN_URL = "https://panel.play.hosting/auth/login"
PANEL_EMAIL = "daisjohncvn3c@gmail.com"
PANEL_PASSWORD = "CD9037025101"
SERVER_URL = "https://panel.play.hosting/server/5ba25eae"


def trigger_panel_action(button_selector):
    with sync_playwright() as p:
        # Launch headless browser with realistic desktop viewport
        browser = p.chromium.launch(
            headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # Step 1: Navigate to login and authenticate
        page.goto(PANEL_LOGIN_URL, wait_until="networkidle")

        # Fill credentials if redirected to login
        if "login" in page.url:
            page.fill('input[type="email"], input[name="username"]', PANEL_EMAIL)
            page.fill('input[type="password"]', PANEL_PASSWORD)
            page.click('button[type="submit"]')
            page.wait_for_timeout(3000)

        # Step 2: Navigate to server dashboard
        page.goto(SERVER_URL, wait_until="networkidle")

        # Step 3: Click targeted control button
        page.click(button_selector)
        page.wait_for_timeout(2000)

        browser.close()


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/wake", methods=["POST"])
def wake():
    try:
        # Pass CSS selector for your panel's Wake button
        trigger_panel_action('button:has-text("Wake")')
        return "<h3>Wake command sent successfully!</h3>"
    except Exception as e:
        return f"<h3>Error triggering wake action: {str(e)}</h3>"


@app.route("/start", methods=["POST"])
def start():
    try:
        # Pass CSS selector for your panel's Start button
        trigger_panel_action('button:has-text("Start")')
        return "<h3>Start command sent successfully!</h3>"
    except Exception as e:
        return f"<h3>Error triggering start action: {str(e)}</h3>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
