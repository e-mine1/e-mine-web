from flask import Flask, request, jsonify
from solc_wrapper import compile_sol, SOLIDITY_TEMPLATE_ROOT
import db
import os

import logging
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'E-Mine1 Backend'


@app.route('/api/requests/<id>', methods=['get'])
def requests_status(id):
    if not id or not db.has_token(id):
        return jsonify(error='invalid id'), 400


    token = db.get_token(id)
    print(token)
    return jsonify(token), 200

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

    propMap = {"token_name": str(payload.get('tokenName')),
               'token_symbol': str(payload.get('symbol')),
               'token_decimals': str(payload.get('decimals')),
               'token_initial_supply': str(payload.get('genesisSupply'))
               }

    contract_template_name = 'MyStandardToken'
    contract_template_path = os.path.join(SOLIDITY_TEMPLATE_ROOT, 'MyStandardToken.sol')

    request_token = db.create_request_token()
    request_id = request_token.get('key')

    #
    # create a new solidity file and compile it
    #
    compile_sol(contract_template_path, contract_template_name,
                propMap, on_compiled_and_deployed, request_id)

    return jsonify(request_token), 200


def render_error(msg):
    return jsonify({'error', msg})


def on_compiled_and_deployed(status, addr, request_id):
    db_status = 'success'
    db_token_addr = addr if status else None
    if not status:
        db_status = 'failed'

    db.update_token(request_id, status=db_status, token_addr=db_token_addr)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
