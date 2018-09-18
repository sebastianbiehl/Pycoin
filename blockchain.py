from functools import reduce
from hashlib import sha256
import json

# Initializing the blockchain

MINING_REWARD = 10

genesis_block = {
    'previous_hash': '',
    'block_depth': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Sebastian'
participants = set({owner})


def hash_block(block):
    return sha256(json.dumps(block).encode()).hexdigest()


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant]
                 for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant]
                    for block in blockchain]
    amount_received = reduce(
        lambda tx_sum, tx_amt: tx_sum + tx_amt[0] if len(tx_amt) > 0 else tx_sum, tx_recipient, 0)
    return amount_received - amount_sent


def get_last_blockchain_value():
    """ Returns last value of the blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add new transaction to the transaction queue.

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: Amount of coins sent with transaction (default = 1.0).
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'block_depth': len(blockchain),
        'transactions': copied_transactions
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns input of the user (transaction amount) as float. """
    # Get  user input, transform it from  string to  float and store in user_input
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount


def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output  blockchain list to console
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    """ Verify blockchain and return True if valid, otherwise False."""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

# While loop for  user interface
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # Add transaction to transaction queue
        if add_transaction(recipient, amount=amount):
            print("Transaction added!")
        else:
            print("Transaction failed ...")
    elif user_choice == '2':
        if mine_block():
            open_transactions.clear()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions valid')
        else:
            print('There are invalid transactions...')
    elif user_choice == 'h':
        # Hack Attack on genesis block
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'block_depth': 0,
                'transactions': [{'sender': 'James', 'recipient': owner, 'amount': 100}]
            }
    elif user_choice == 'q':
        # End loop and exit program
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print(f'Balance of {owner}: {get_balance(owner):6.2f}')


print('Done!')
