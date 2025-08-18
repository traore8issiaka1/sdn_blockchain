from web3 import Web3
import json
import time
from flask_socketio import SocketIO

# Connexion à Hardhat ou Ganache
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# Adresse du contrat (remplace par l’adresse réelle de déploiement)
contract_address = Web3.to_checksum_address("0x47Bc01D6de9a059E9c4a7DF30CaB78a3886d74dA")

# Charger l'ABI compilée
with open('artifacts/contracts/EventLogger.sol/EventLogger.json') as f:
    contract_json = json.load(f)
    abi = contract_json['abi']

# Instancier le contrat
contract = w3.eth.contract(address=contract_address, abi=abi)

def listen_events(socketio: SocketIO):
    print("⏳ Démarrage de l’écoute des événements EventLogger…")
    event_filter = contract.events.EventLogged.create_filter(fromBlock='latest')

    while True:
        for event in event_filter.get_new_entries():
            hash_val = event['args']['hash']
            details = event['args']['details']
            timestamp = event['args']['timestamp']
            block_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

            log_data = {
                'hash': hash_val,
                'details': details,
                'timestamp': block_time
            }

            print("✅ Événement capté :", log_data)
            socketio.emit('new_tx_event', log_data)

        time.sleep(2)
