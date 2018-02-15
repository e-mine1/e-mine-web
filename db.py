from tinydb import TinyDB, Query
import os
import uuid

from datetime import datetime, timezone

DB_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db.json')

db = TinyDB(DB_LOCATION)
Creation = Query()


def _get_now():
    return datetime.now(timezone.utc).astimezone().isoformat()


def create_request_token():
    key = uuid.uuid4()
    date = _get_now(),
    entry = {
        'key': key,
        'status': 'pending',
        'token_addr': None,
        'created': date,
        'updated': date,
        'version': 0
    }
    db.insert(entry)
    return entry


def has_token(key):
    return db.search(Creation.key == key) is not None


def update_token(key, status=None, token_addr=None):
    results = db.search(Creation.key == key)
    if results:
        token = results[0]
        change = False
        if status:
            token.status = status
            change = True
        if token_addr:
            token.token_add = token_addr
            change = True

        if change:
            token.updated = _get_now()
