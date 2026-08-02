from flask import Flask, jsonify, render_template_string
import os
import socket

app = Flask(__name__)

# Basic HTML Template for the homepage
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Demo App</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background-color: #1e293b;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        h1 { color: #38bdf8; margin-bottom: 0.5rem; }
        p { color: #94a3b8; font-size: 0.95rem; }
        .status {
            display: inline-block;
            background-color: #22c55e;
            color: #052e16;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-weight: bold;
            font-size: 0.85rem;
            margin-top: 1rem;
        }
        .info {
            margin-top: 1.5rem;
            text-align: left;
            background: #0f172a;
            padding: 1rem;
            border-radius: 8px;
            font-family: monospace;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 App Online</h1>
        <p>CI/CD Pipeline & Docker Automation Demo</p>
        <div class="status">HEALTHY</div>
        <div class="info">
            <strong>Host:</strong> {{ hostname }}<br>
            <strong>Environment:</strong> {{ env }}
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    hostname = socket.gethostname()
    env = os.getenv("APP_ENV", "production")
    return render_template_string(HTML_TEMPLATE, hostname=hostname, env=env)

@app.route("/api/v1/status")
def status():
    return jsonify({
        "status": "success",
        "message": "API is operational",
        "container_id": socket.gethostname()
    }), 200

# Health check route for Docker / Kubernetes liveness probes
@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
