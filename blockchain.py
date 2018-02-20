import hashlib as hasher
import datetime as date


# Define what a block is
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) +
                   str(self.timestamp) +
                   str(self.data) +
                   str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()


# Generate genesis block
def create_genesis_block():
    return Block(0, date.datetime.now(), {"text": "Genesis Block", "proof-of-work": 1}, "0")


# Generate next block for loop
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "This is block " + str(this_index)
    this_previous_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_previous_hash)


def test_blockchain():
    # Create the blockchain.py itself and add the genesis block
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

    # Add 20 blocks to the chain
    for i in range(0, 20):
        block_to_add = next_block(previous_block)
        blockchain.append(block_to_add)
        previous_block = block_to_add

        print("Block #{} has been added to the blockchain.py".format(block_to_add.index))
        print("Hash: {}\n".format(block_to_add.hash))


blockchain = [create_genesis_block()]

#test_blockchain()