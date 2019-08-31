import datetime
import hashlib
from block import Block
import requests
from urllib.parse import urlparse
import json
from flask import jsonify
from wallet import Wallet

class Blockchain:
    def __init__(self):
        self.chain = [Block.generate_genesis()]
        self.nodes = set()
        self.data = []

    def addblock(self):
        block = Block.mine(self.chain[len(self.chain) - 1] , self.data)

        self.chain.append(block)
        self.data = []
        network = self.nodes
        for node in network:
            response = requests.get('http://'+node+'/replace_chain')


    def add_transaction(self , transaction , public_key , signature):
        verified = Wallet.verify(transaction , public_key , signature)

        if verified:
            self.data.append(json.dumps(transaction))
            network = self.nodes

            for node in network:
                response = requests.post('http://'+node+'/update_transactions' , params = transaction)

            return True
        else:
            return False

    def update_transactions(self):
        network = self.nodes
        for node in network:
            transactions = requests.get('http://'+node+'/get_transactions')
            if transactions.status_code == 200:
                transaction = transactions.json()['transactions']
                latest = transaction[len(transaction)-1]
                self.data.append(latest)
        return True, 200

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get('http://'+node+'/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                newchain = []

                for block in chain:
                    newchain.append(Block(block['timestamp'] , block['nonce'] ,block['data'] , block['curhash'] , block['previous_hash']) )
                print(self.is_chain_valid(newchain))
                if length > max_length and self.is_chain_valid(newchain):
                    max_length = length
                    longest_chain = newchain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def is_chain_valid(self , chain):
        for i in (1,len(chain)-1):
            block = chain[i]
            previous_block = chain[i-1]

            if(previous_block.hash() != block.previous_hash):
                return False
            hash_operation = hashlib.sha256(str(block.timestamp+ str(block.nonce) + json.dumps(block.data) + block.previous_hash).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

        return True
