from flask import Flask, request, jsonify
from solc_wrapper import generateSolFile, compileSol
import logging

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/tokens/create', ['post'])
def tokens_create():
    if request.get_json() is None:
        return jsonify(error='No payload given :/'), 400

    payload = request.get_json()
    required = ['tokenName', 'symbol', 'maxSupply', 'decimals', 'genesisSupply']
    for r in required:
        if r not in payload:
            return jsonify(error='Missing required param {} in request'.format(r)), 400

    tokenName = payload.get('tokenName')
    symbol = payload.get('symbol')
    maxSupply = payload.get('maxSupply')
    decimals = payload.get('decimals')
    genesisSupply = payload.get('genesisSupply')

    solFile = generateSolFile(tokenName, symbol, maxSupply, decimals, genesisSupply)
    solBinPath = compileSol(solFile)

    pass

def render_error(msg):
    return jsonify({'error', msg})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

