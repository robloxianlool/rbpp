import random
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

server_on = True
logged_in_user = None

def generate_code():
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choices(chars, k=6))

current_code = generate_code()

@app.route('/status')
def status():
    return jsonify({"status": "yes" if server_on else "no"})

@app.route('/code')
def code():
    return jsonify({"code": current_code})

@app.route('/verify', methods=['POST'])
def verify():
    global logged_in_user
    data = request.json
    code = data.get("code")
    user = data.get("user")
    if code == current_code:
        logged_in_user = user
        return jsonify({"result": "confirmed", "user": user})
    else:
        return jsonify({"result": "denied"})

@app.route('/logout', methods=['POST'])
def logout():
    global logged_in_user, current_code
    logged_in_user = None
    current_code = generate_code()
    return jsonify({"result": "logged out", "new_code": current_code})

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    threading.Thread(target=run_server).start()
