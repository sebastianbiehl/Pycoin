from utility.hash_util import hash_str_256, hash_block

from wallet import Wallet


class Verification:

    @staticmethod
    def valid_nonce(transactions, last_hash, nonce, difficulty):
        guess = (str([tx.to_ordered_dict for tx in transactions]) +
                 str(last_hash) + str(nonce)).encode()
        guess_hash = hash_str_256(guess)
        return guess_hash[0:difficulty] == '0' * difficulty

    @classmethod
    def verify_chain(cls, blockchain, difficulty):
        """ Verify blockchain and return True if valid, otherwise False."""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                return False
            if not cls.valid_nonce(block.transactions[:-1], block.previous_hash, block.nonce, difficulty):
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        if check_funds:
            sender_balance = get_balance()
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])
