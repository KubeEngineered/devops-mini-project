from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    """Default landing route."""
    return jsonify({
        "status": "success",
        "message": "Welcome to the DevOps Mini-Project API!",
        "version": "1.0.0"
    })


@app.route("/health")
def health_check():
    """Health check endpoint useful for DevOps monitoring/containers."""
    return jsonify({
        "status": "healthy",
        "uptime": "OK"
    }), 200


if __name__ == "__main__":
    # Runs the app locally on http://127.0.0.1:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
