import datetime as date

from flask import Flask, json, request
from blockchain import Block, blockchain

node = Flask(__name__)

this_nodes_transactions = []
miner_address = "stan"


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


@node.route('/mine', methods=['GET'])
def mine():
    this_nodes_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )

    last_block = blockchain[len(blockchain) - 1]
    new_block_data = {
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
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


node.run()