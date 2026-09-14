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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": """remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InNLek1NdEFCVno3NjB2UlozTDRkcHc9PSIsInZhbHVlIjoidmxURkhHVTV5dmxEZ2ZaNldERlRsTDg0K2dzV0pLd2NkOGt4SzA4MDVNZjgwVW5xbHRPQnkxSHJLS2xpcXZ3Vnd1SmFKZWduYy8weEZQVS9tcGxkM2xPNHEzc2RHUTFNK3R2U1MxWjl6bmh1dXpJVnlYd3lMSDZrSzlRNzZRVlNBQWRZT0gycXFDK1YyaUd6S0pWS2N4K1U4d3EvcWdiYlRPK2NGODRaL2lZQlg4dWF5VTBvRE56RWJSTFdHSE1UU000UkZvQTgzNUhUZFdieURBeGM3aHF1aHdTQk9VbkN3QlEzSG5pVDBLST0iLCJtYWMiOiI1YzgzY2FkZGFiYjMyMzVhOTQ2OTExN2NkMzYxOWNhZmU5NjJlNDNkYTdlMWFhOTc5MzdjOWQwYjhkNTgzZGIyIiwidGFnIjoiIn0%3D; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%225a2dc19a-e443-41c2-bf1f-d3b2cc52f963%5C%22%2C%5B1789401878%2C589000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol_OMVoMCwOizf2j7uqczEa9XbjZSr18533b_17LZIYRCHCqXQCK5-IwTJJKuNYl3K2S-pKSgccLbkVQnCZR2eWm-Kt3G5qFR1E0AT1J5QkN14xFZi8XX0xdfDblBvhUaBppiVZJ4DrsYCvGdBdMlh7uzllBKA%3D%3D%22%5D%5D; __gads=ID=84c18b4ca3869f89:T=1789401869:RT=1789403675:S=ALNI_MY1buMEO-nsF9YEVDqG4Mo-SqAt-A; __gpi=UID=00001570c24ddd7d:T=1789401869:RT=1789403675:S=ALNI_MZFTrPax0SMwIIzchQtx7S75FpDFQ; __eoi=ID=875210249115ac75:T=1789401869:RT=1789403675:S=AA-AfjbjBzgTyb6M97XrDJt7YuRz; cf_clearance=6wquXFmbO7JktheN3tc06H0uDsluxQJ8du5oTfXynYw-1789403686-1.2.1.1-iSHVSQ1e1zG7WGu9lG3hq.0AWfZALnjDGCzGQfTDNb_DVL.0mrg4ftyMrXNl2MYdIs6pZakCrp.dLDS7BniZTe9GimumN3ZgWBlD.CYeYXYWODlqLj2fdvm9WhSYrWr8Qp6T2SpFsxdlgf5BhD675Qat0J0AGrmmlUm8hat2o_StRJaRfelcEMAGH0dRB2WlqAQ0xXpW_SJSa7acpWBpoT9BRXaYkhNrfPrhQKoHzxLjPQ3NQFUQR64iQ4kCnnJJYYcpzxM.vm_iUPqEZKZ.uwFs_g7TfnjCNmCbr0DY3vW_6Wts_78fEMpaxi.2YIHgLHEUXNqAScVVXjuJivAh8GDLgybJEbnBuCmXFy4r_N3srqPgbLLPEkPrnZvNG28mFLxVZvAaV90awsC0ZYD2Or2Akr8pN47OKUm2GmRni6nRANSpqUficuNKVAYvUJJsXlf37FM9iX7RqYZCQacSB92aOOo.eDiaCtqBmvYGnVLe9IwYB2fBmh79jPGXZf8E; XSRF-TOKEN=eyJpdiI6Ik8vMkl1c1ZKNTIzNTNNK3hTR3VQNFE9PSIsInZhbHVlIjoiekdMUWZ4d3lJUnZEWktMQUVpTVd1b0k0Uk9HZlNSMzRFb1pWRmR1ZDhZZTc3a1BIVHZmbVFBSHRvNkNucCtoY3VKVGpENWJpMmNIdXYva3FYVnk3TFRMelBoNXp1YWpYclV4UnhCK1FFYk1XNStONmtiY1VUdTV4SU5OeUF5KzgiLCJtYWMiOiI5ZmMzYWI5ZGFmYzljMGIyYmRkZGRjNjkwNWEyNTEwYTZiZTA5N2M1Mzk3ZjhhZjJhZjAwZGY4OTIzOWUyN2FhIiwidGFnIjoiIn0%3D; play_hosting_session=eyJpdiI6IjRLY0JXeGFhVkZLdkM0eXpjRVdxM1E9PSIsInZhbHVlIjoiUkJoU1NITzYzbzJwUVhGbmo1TVBMZ2lBeUtRdElMZG5WQ2dlR0NQUlZKbE4zWWlJNGlsMnMwNnFYL2RJYVdsNzRmUXNaS040UHRRRkZreHV4Y0NqZW9SeVJSZ3ZIdzhYWS9LQllzSGVWVU1mU2tZOWpmaU9xc0lSMU5wcFoxSFYiLCJtYWMiOiI3MjQzODRiYWE5NTU1NTE2ZGMyOWY2ZWIzMjY4MDc4ODhhMjg2MmVkZTkxNjE3YzJjNjkzOTA0NmIwYjBjZjdmIiwidGFnIjoiIn0%3D""",
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
