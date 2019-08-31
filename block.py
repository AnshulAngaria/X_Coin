import datetime
import hashlib
import json

class Block:
    def __init__(self ,  timestamp, nonce , data , hash , previous_hash):
        self.timestamp = timestamp
        self.nonce = nonce
        self.data = data
        self.curhash = hash
        self.previous_hash = previous_hash

    def hash(self):
        print(json.dumps(self.data))
        return hashlib.sha256( (self.timestamp+ str(self.nonce) + json.dumps(self.data)+self.previous_hash).encode()).hexdigest()

    def generate_genesis():
        hash = hashlib.sha256(str('Today'+str(0)+ json.dumps('data') + 'xyz').encode()).hexdigest()
        return Block('Today' ,0, 'data' , hash , 'xyz')


    def mine(lastblock , data):

        timestamp = str(datetime.datetime.now())
        nonce = 0;

        previous_hash = lastblock.curhash
        while(hashlib.sha256((timestamp +str(nonce) +  json.dumps(data) + previous_hash).encode()).hexdigest()[0:4] != "0000"):
            nonce+=1


        return Block(timestamp , nonce , data , hashlib.sha256((timestamp +str(nonce) +  json.dumps(data) + previous_hash).encode()).hexdigest() , previous_hash)
