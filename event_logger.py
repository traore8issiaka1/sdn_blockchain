from web3 import Web3
import requests
import json
import hashlib
import time
from datetime import datetime

# ONOS
ONOS_URL = "http://localhost:8181/onos/v1/flows"
ONOS_AUTH = ("onos", "rocks")

# Ethereum
ETH_NODE = "http://127.0.0.1:8545"
CONTRACT_ADDRESS = "0x47Bc01D6de9a059E9c4a7DF30CaB78a3886d74dA"
ABI_PATH = "/home/sdn/event-logger/artifacts/contracts/EventLogger.sol/EventLogger.json"  # Remplace ici

# Init Web3 et contrat
w3 = Web3(Web3.HTTPProvider(ETH_NODE))
with open(ABI_PATH) as f:
    CONTRACT_ABI = json.load(f)["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
account = w3.eth.accounts[0]

previous_flows = set()

def hash_event(flow):
    m = hashlib.sha256()
    m.update(json.dumps(flow, sort_keys=True).encode())
    return m.hexdigest()

def describe_event(flow):
    return f"Flow {flow['id']} on device {flow['deviceId']}"

while True:
    try:
        r = requests.get(ONOS_URL, auth=ONOS_AUTH)
        r.raise_for_status()
        flows = r.json().get("flows", [])

        current_ids = set(f["id"] for f in flows)
        new_ids = current_ids - previous_flows

        for flow in flows:
            if flow["id"] in new_ids:
                print(f"[{datetime.now()}]  Nouveau flow détecté : {flow['id']}")
                event_hash = hash_event(flow)
                details = describe_event(flow)
                print(f" Détails: {details}")
                print(f" Hash: {event_hash}")

                # Transaction
                tx_hash = contract.functions.logEvent(event_hash, details).transact({"from": account})
                print(f" Transaction envoyée : {tx_hash.hex()}")

        previous_flows = current_ids
        time.sleep(5)

    except KeyboardInterrupt:
        print(" Interrompu par l'utilisateur.")
        break
    except Exception as e:
        print(f" Erreur : {e}")
        time.sleep(5)
