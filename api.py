"""
API REST da blockchain
"""
from flask import Flask, request, jsonify
from .chain import Blockchain
from .wallet_manager import WalletManager
from .config import BLOCKCHAIN_CONFIG

app = Flask(__name__)
blockchain = Blockchain()
wallet_manager = WalletManager()

@app.route('/wallet/new', methods=['POST'])
def create_wallet():
    data = request.get_json()
    name = data.get('name', '')
    address = wallet_manager.create_wallet(name)
    return jsonify({'address': address, 'message': 'Wallet created successfully'})

@app.route('/wallet/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance})

@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required = ['from_address', 'to_address', 'amount']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing values'}), 400

    success = blockchain.add_transaction(
        data['from_address'],
        data['to_address'],
        float(data['amount'])
    )
    
    if success:
        return jsonify({'message': 'Transaction added successfully'})
    return jsonify({'error': 'Failed to add transaction'}), 400

@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    if 'miner_address' not in data:
        return jsonify({'error': 'Missing miner address'}), 400

    success, message = blockchain.mine_pending_transactions(data['miner_address'])
    if success:
        return jsonify({'message': message})
    return jsonify({'error': message}), 400

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.to_dict())
    return jsonify({
        'chain': chain_data,
        'length': len(chain_data)
    })

def start_api():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    start_api()