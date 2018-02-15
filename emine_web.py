from flask import Flask, request, jsonify
from solc_wrapper import generateSolFile, compileSol
import logging
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'E-Mine1 Backend'


@app.route('/api/tokens/create', methods=['post'])
def tokens_create():
    try:
        if request.get_json() is None:
            return jsonify(error='No payload given :/'), 400
    except Exception:
        return jsonify(error='Invalid content-type given'), 500

    print('here')
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

    return jsonify(status='success'), 200
    pass


def render_error(msg):
    return jsonify({'error', msg})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
