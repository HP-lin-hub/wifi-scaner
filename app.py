from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading, time
from scanner import parse_iw_scan
import subprocess, re

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

selected_interface = None
selected_freqs = []
networks_data = []

@app.route("/interfaces")
def get_interfaces():
    try:
        result = subprocess.run(["iw", "dev"], capture_output=True, text=True)
        interfaces = re.findall(r"Interface (\w+)", result.stdout)
        return jsonify(interfaces)
    except Exception as e:
        print(f"Error getting interfaces: {e}")
        return jsonify([])

@app.route("/start", methods=["POST"])
def start_scan():
    global selected_interface, selected_freqs
    data = request.json
    iface = data.get("interface")
    freqs = data.get("freqs", [])
    if iface:
        selected_interface = iface
        selected_freqs = freqs
        return "", 200
    return "Interface not selected", 400

@app.route("/stop", methods=["POST"])
def stop_scan():
    global selected_interface
    selected_interface = None
    return "", 200

def scanner_loop():
    global networks_data
    while True:
        if selected_interface:
            try:
                networks_data = parse_iw_scan(selected_interface, selected_freqs)
                socketio.emit("update", networks_data)
            except Exception as e:
                print(f"Error in scanning loop: {e}")
        time.sleep(2)

threading.Thread(target=scanner_loop, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)