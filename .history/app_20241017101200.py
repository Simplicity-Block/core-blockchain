import threading
import time
from urllib.parse import urlparse
from uuid import uuid4
import flask
import requests
from blockchain import Blockchain
from database import BlockchainDb
from flask_cors import CORS  # Import CORS

app = flask.Flask(__name__)
from flask import Flask, copy_current_request_context, g, request, jsonify

# Enable CORS for the entire Flask app
CORS(app)

blockchain = Blockchain()

@app.route('/hello', methods=['GET'])
def hello():
    return flask.jsonify({
        'nodes': list(blockchain.nodes),
        'length': len(list(blockchain.nodes))
    })


@app.route('/chain', methods=['GET'])
def chain():
    return flask.jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    })


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = flask.request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['transaction', 'digital_signature', 'public_key']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index, error = blockchain.new_transaction(values['transaction'], values['public_key'], values['digital_signature'])
    if index is not None:
        response = {'message': f'Transaction will be added to Block {index}'}
    else:
        response = {'message': error}
    return flask.jsonify(response), 201


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = flask.request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        print("this is parent node", "simplicity_server1.onrender.com")
        blockchain.register_node(node, "simplicity_server1.onrender.com")

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return flask.jsonify(response), 201


@app.route('/nodes/update_nodes', methods=['POST'])
def update_nodes():
    values = flask.request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        print("this is parent node", "simplicity_server1.onrender.com")
        if node not in blockchain.nodes:
            blockchain.nodes.add(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return flask.jsonify(response), 201

@app.route('/nodes/update_ttl', methods=['POST'])
def update_ttl():
    values = flask.request.get_json()
    print(values)
    update_nodes = values.get('updated_nodes')
    print("this is the updated nodes in the request", update_nodes)
    node = values.get('node')
    if update_nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    blockchain.updateTTL(update_nodes , node )
    response = {
        'message': 'The TTL of nodes have been updated',
        'total_nodes': list(blockchain.nodes),
    }
    return flask.jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return flask.jsonify(response), 200


@app.route('/nodes/update_block', methods=['POST'])
def update_block():
    block = flask.request.get_json()
    print("this is block", block)
    if blockchain.hash(block) in blockchain.hash_list:
        return flask.jsonify(f"Already added Block in the network {block}"), 200
    else:
        for transaction in block['transactions']:
            if transaction in blockchain.current_transactions:
                blockchain.current_transactions.remove(transaction)

        blockchain.chain.append(block)
        blockchain.hash_list.add(blockchain.hash(block))

        # send data to the known nodes in the network
        for node in blockchain.nodes:
            requests.post(f'http://{node}/nodes/update_block', json=block, timeout=5)
            requests.post(f'http://{node}/nodes/update_nodes', json={
                "nodes": list(blockchain.nodes)
            })

    return flask.jsonify(f"Added Block to the network {block}"), 200


@app.route('/nodes/update_transaction', methods=['POST'])
def update_transaction():
    transaction = flask.request.get_json()

    if transaction.get('id') in [t.get('id') for t in blockchain.current_transactions]:
        return flask.jsonify({"message": f"Transaction already in the network", "transaction": transaction}), 200

    blockchain.current_transactions.append(transaction)
    blockchain.miner()

    # Send data to the known nodes in the network
    failed_nodes = []
    for node in blockchain.nodes:
        try:
            response = requests.post(f'http://{node}/nodes/update_transaction', json=transaction, timeout=5)
            if response.status_code != 200:
                failed_nodes.append({"node": node, "reason": f"Non-200 status code: {response.status_code}"})
        except requests.exceptions.RequestException as e:
            failed_nodes.append({"node": node, "reason": str(e)})

    if failed_nodes:
        app.logger.warning(f"Failed to send transaction to some nodes: {failed_nodes}")

    return flask.jsonify({
        "message": "Added transaction to the network",
        "transaction": transaction,
        "failed_nodes": failed_nodes
    }), 200


@app.route('/nodes/update_chain', methods=['POST'])
def update_chain():
    response = flask.request.get_json()
    blockchain.chain = []
    parent_node = response[1]
    blockchain.nodes.add(parent_node)
    chain_list = response[0]
    hash_list = response[2]
    blockchain.hash_list = set(hash_list)
    for chain in chain_list:
        if chain not in blockchain.chain:
            blockchain.chain.append(chain)

    return flask.jsonify(f"Added Chain to the network {chain_list} and nodes are {blockchain.nodes}"), 200


@app.route('/delete_node', methods=['POST'])
def delete_chain():
    response = flask.request.get_json()
    blockchain.nodes.remove(response.get("node"))

    return flask.jsonify(f"removed Node from the network"), 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    database = BlockchainDb()
    database.save_blockchain(blockchain)

    host_url = getattr(g, 'host_url', None)  # Get the host URL safely
    if host_url:
        for node in blockchain.nodes:
            try:
                requests.post(f'http://{node}/delete_node', json={"node": host_url}, timeout=5)
            except requests.exceptions.RequestException as e:
                print(f"Error notifying node {node}: {e}")


def register_node(port):
    print(f"Registering node with port {port}...")
    print("nodes" ,blockchain.nodes)
    print("nodes type" ,type(blockchain.nodes))
    print("chain" ,blockchain.chain)
    print("chain type" ,type(blockchain.chain))
    blockchain.register('simplicity_server1.onrender.com')


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    threading.Thread(target=register_node, args=[port], daemon=True).start()
    app.run(host='0.0.0.0', port=port)
