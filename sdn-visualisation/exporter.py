from flask import Flask, Response
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Un compteur Prometheus
flow_counter = Counter('sdn_new_flows', 'Nombre de nouveaux flux détectés')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

# Exemple fictif d'appel à incrémenter lors d’un nouvel event
@app.route('/new-flow')
def new_flow():
    flow_counter.inc()
    return "Flow enregistré !"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
