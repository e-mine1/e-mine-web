from tinydb import TinyDB, Query
import os
import uuid
import base64

from datetime import datetime, timezone

DB_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db.json')

db = TinyDB(DB_LOCATION)
Creation = Query()


def _get_now():
    return str(datetime.now(timezone.utc).isoformat())


def create_request_token():
    key = str(uuid.uuid4())
    d = str(_get_now())
    entry = {
        'key': key,
        'status': 'pending',
        'token_addr': None,
        'token_abi': None,
        'created': d,
        'updated': d,
        'version': 0
    }
    print('create request token: ' + key)
    db.insert(entry)
    return entry


def has_token(key):
    res = db.search(Creation.key == key)

    return len(res) > 0


def get_token(key):
    res = db.search(Creation.key == key)
    if len(res) > 0:
        return res[0]
    else:
        return None


def update_token(key, status=None, token_addr=None, token_abi=None):
    results = db.search(Creation.key == key)
    if results:
        token = results[0]
        change = False
        if status:
            token['status'] = status
            change = True
        if token_addr:
            token['token_addr'] = token_addr
            change = True

        if token_abi:
            token['token_abi'] = base64.b64encode(token_abi.encode()).decode('utf-8')
            change = True

        if change:
            token['updated'] = _get_now()
            token['version'] = int(token['version']) + 1
            print('updated request token: ' + key)
            db.update(token, Creation.key == key)
