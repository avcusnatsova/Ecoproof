import hashlib
import json
import os
from time import time
import pandas as pd

# File to store blockchain data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

CHAIN_FILE = os.path.join(DATA_DIR, "blockchain_data.json")


# -----------------------------
# BLOCK CLASS
# -----------------------------
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()
        self.row_hash = self.compute_row_hash(data) if isinstance(data, dict) else None

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def compute_row_hash(self, row_data):
        row_string = json.dumps(row_data, sort_keys=True).encode()
        return hashlib.sha256(row_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "row_hash": self.row_hash
        }


# -----------------------------
# BLOCKCHAIN CLASS
# -----------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        genesis_block = Block(0, time(), {"info": "Genesis Block"}, "0")
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        index = self.last_block.index + 1
        timestamp = time()
        previous_hash = self.last_block.hash

        new_block = Block(index, timestamp, data, previous_hash)
        self.chain.append(new_block)
        self.save_chain()

        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def save_chain(self):
        with open(CHAIN_FILE, "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_chain(self):
        try:
            if os.path.exists(CHAIN_FILE):
                with open(CHAIN_FILE, "r") as f:
                    chain_data = json.load(f)

                self.chain = []

                for block_data in chain_data:
                    block = Block(
                        block_data['index'],
                        block_data['timestamp'],
                        block_data['data'],
                        block_data['previous_hash']
                    )
                    block.hash = block_data['hash']
                    block.row_hash = block_data.get("row_hash")
                    self.chain.append(block)
            else:
                self.create_genesis_block()
                self.save_chain()

        except Exception as e:
            print(f"Error loading blockchain: {e}")
            self.chain = []
            self.create_genesis_block()
            self.save_chain()

    def is_row_logged(self, row_data):
        row_hash = hashlib.sha256(
            json.dumps(row_data, sort_keys=True).encode()
        ).hexdigest()

        return any(block.row_hash == row_hash for block in self.chain)

    def chain_to_dataframe(self):
        return pd.DataFrame([block.to_dict() for block in self.chain])