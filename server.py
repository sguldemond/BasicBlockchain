import datetime as date

from flask import Flask, json, request
from blockchain import Block, blockchain

# local variables
node = Flask(__name__)
this_nodes_transactions = []
miner_address = "stan"


# verify if sender has sufficient amount of coins &
# if coin is not already spend
#
# in this example anything can be added as 'transaction'
# how can coins be validated?
@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_nodes_transactions.append(new_txion)

        print("New transaction")
        print("FROM: {}".format(new_txion['from']))
        print("TO {}".format(new_txion['to']))
        print("AMOUNT {}\n".format(new_txion['amount']))

        return "Transaction submission succesful\n"


def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor


# based of the implementation of 'mining' in tutorial,
# in this method only a block is created
#
# proof of work could be added to the block data including a reward for the miner in the form of a coin
#
# how to send distribute generated block to different nodes?
@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']

    this_nodes_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )

    proof = proof_of_work(last_proof)

    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
    }

    new_block_index = last_block.index + 1
    new_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    this_nodes_transactions[:] = []

    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    blockchain.append(mined_block)

    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = []
    for block in blockchain:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = block.data
        block_hash = block.hash
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }
        chain_to_send.append(block)

    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send


def distribute_block():
    return


node.run()
