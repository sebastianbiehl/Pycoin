from hashlib import sha256
import json


def hash_str_256(string):
    return sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [
        tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_str_256(json.dumps(hashable_block, sort_keys=True).encode())
