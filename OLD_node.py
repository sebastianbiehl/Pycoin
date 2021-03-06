from uuid import uuid4

from blockchain import Blockchain
from wallet import Wallet
from utility.verification import Verification


class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ')
        return user_input

    def print_line(self):
        return print('-' * 20)

    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        # Output  blockchain list to console
        for block in self.blockchain.chain:
            print(block)
            self.print_line()

    def get_transaction_value(self):
        """ Returns input of the user (transaction amount) as float. """
        # Get  user input, transform it from  string to  float and store in user_input
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount please: '))
        return tx_recipient, tx_amount

    def listen_for_input(self):
        waiting_for_input = True
        # While loop for  user interface
        while waiting_for_input:
            self.print_line()
            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transaction validity')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save Keys')
            print('q: Quit')
            user_choice = self.get_user_choice()
            self.print_line()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                # Add transaction to transaction queue
                signature = self.wallet.sign_transaction(
                    self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print("Transaction added!")
                else:
                    print("Transaction failed ...")
                self.print_line()
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed. Got no wallet?')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions valid')
                else:
                    print('There are invalid transactions...')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == 'q':
                # End loop and exit program
                waiting_for_input = False
            elif user_choice == '7':
                self.wallet.save_keys()
            else:
                print('Input was invalid, please pick a value from the list!')
            if not Verification.verify_chain(self.blockchain.chain, self.blockchain.difficulty):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                break
            print(
                f'Balance of {self.wallet.public_key}: {self.blockchain.get_balance():6.2f} ')

        print('Done!')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
