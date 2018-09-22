from functools import reduce
from hashlib import sha256
from collections import OrderedDict
import json

from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

MINING_REWARD = 10


class Blockchain:

    def __init__(self, hosting_node_id):
        # Initializing the blockchain
        genesis_block = Block(0, '',  [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id
        self.difficulty = 4

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['block_depth'], block['previous_hash'], converted_tx, block['nonce'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            print('Exception occured...')
            pass

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [
                    Block(block_el.block_depth, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.nonce, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        nonce = 0
        while not Verification.valid_nonce(self.__open_transactions, last_hash, nonce, self.difficulty):
            nonce += 1
        return nonce

    def get_balance(self):
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                     for block in self.__chain]
        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                        for block in self.__chain]
        amount_received = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_recipient, 0)
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """ Returns last value of the blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Add new transaction to the transaction queue.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: Amount of coins sent with transaction (default = 1.0).
        """

        if self.hosting_node == None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        if self.hosting_node == None:
            return False
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        nonce = self.proof_of_work()
        reward_transaction = Transaction(
            'MINING', self.hosting_node, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, nonce)
        for tx in block.transactions:
            if not Wallet.verify_transaction(tx):
                return False
        copied_transactions.append(reward_transaction)
        self.__chain.append(block)
        self.__open_transactions.clear()
        self.save_data()
        return True
