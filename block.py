from time import time


class Block:
    def __init__(self, block_depth, previous_hash, transactions, nonce, timestamp=None):
        self.block_depth = block_depth
        self.previous_hash = previous_hash
        self.timestamp = time() if timestamp is None else timestamp
        self.transactions = transactions
        self.nonce = nonce

    def __repr__(self):
        return f'Block: {self.block_depth}\nPrevious Hash: {self.previous_hash}\nNonce: {self.nonce}\nTransactions: {self.transactions}\nTimestamp: {self.timestamp}'
