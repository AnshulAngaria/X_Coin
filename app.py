from flask import Flask, jsonify, request
import requests
from blockchain import Blockchain
from block import Block
import json
from wallet import Wallet

app = Flask(__name__)

blockchain = Blockchain()
wallet = Wallet()

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    chain=[]
    for block in blockchain.chain:
        chain.append({
        'timestamp':block.timestamp,
        'nonce': block.nonce,
        'data' : block.data,
        'curhash': block.curhash,
        'previous_hash': block.previous_hash
        })

    response ={
    'chain': chain,
    'length': len(blockchain.chain)
    }
    return jsonify(response),200


@app.route('/mine'  , methods = ['GET'])
def mineblock():

    blockchain.addblock()
    response = {'message': f'This block is mined'}
    return jsonify(response), 201


@app.route('/add_transaction' , methods = ['POST'])
def add_transaction():
    data = request.get_json()

    signature = wallet.signature(json.dumps(data))

    print(data)
    added = blockchain.add_transaction(data , wallet.public_key , signature)
    if added:
        response = {
        'message': 'transaction added'
        }
        return jsonify(response) , 201
    else:
        response = {
        'message': 'failed to add transaction'
        }
        return jsonify(response) , 500

@app.route('/get_transactions' , methods = ['GET'])
def get_transactions():
    response = {'transactions' : blockchain.data}
    return jsonify(response), 200

@app.route('/update_transactions' , methods = ['POST'])
def add():
    blockchain.update_transactions()
    response = {'message':'transactions upated'}
    return jsonify(response) , 200

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Xcoin Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    blockchain.data = []
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.'}
    else:
        response = {'message': 'All good. The chain is the largest one.'}
    return jsonify(response), 200





app.run(host = '0.0.0.0', port = 5000)
