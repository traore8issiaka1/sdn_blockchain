from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from blockchain_listener import listen_events
import time, threading, random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

history = []  # garder les événements en mémoire pour la démo

def generate_events():
    devices = ['of:0000000000000001', 'of:0000000000000002', 'of:0000000000000003']
    while True:
        flow_id = random.randint(281475000000000, 281479000000000)
        device = random.choice(devices)
        tx_hash = ''.join(random.choices('abcdef0123456789', k=64))
        block_hash = ''.join(random.choices('abcdef0123456789', k=64))
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        event = {
            'timestamp': timestamp,
            'flow_id': flow_id,
            'device': device,
            'tx_hash': tx_hash,
            'block_hash': block_hash
        }

        history.insert(0, event)  # dernier en premier
        if len(history) > 1000:
            history.pop()

        socketio.emit('new_event', event)
        time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/history')
def get_history():
    device = request.args.get('device')
    if device:
        filtered = [e for e in history if e['device'] == device]
    else:
        filtered = history
    return jsonify(filtered)

if __name__ == '__main__':
    # Thread générant des événements réseau aléatoires
    t_gen = threading.Thread(target=generate_events)
    t_gen.daemon = True
    t_gen.start()

    # Thread écoutant la blockchain (événements smart contract)
    t_bc = threading.Thread(target=listen_events, args=(socketio,))
    t_bc.daemon = True
    t_bc.start()

    # Démarrage serveur Flask + SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
