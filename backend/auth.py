import base64
from tkinter.messagebox import NO
import bcrypt
import datetime
import hashlib
import secrets

import jwt

from db import USERS_DB


def validate_user_login(username, password):
    user = None
    user_id = None
    for id, user_data in USERS_DB.items():
        if user_data["username"] == username:
            user = user_data
            user_id = id
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return user, user_id
    else:
        return None, None


def generate_fingerprint():
    fingerprint = secrets.token_bytes(16)
    fingerprint_hash = base64.urlsafe_b64encode(
        hashlib.sha256(fingerprint).digest()
    ).decode()
    return fingerprint, fingerprint_hash


def generate_access_token(user_id, fingerprint_hash, now, private_key):
    return jwt.encode(
        {
            "iss": "myauthserver.com",
            "iat": now,
            "exp": now + datetime.timedelta(minutes=15),
            "user_id": user_id,
            "fingerprint": fingerprint_hash,
        },
        private_key,
        algorithm="RS256",
    )


def generate_refresh_token(fingerprint_hash, now, private_key):
    return jwt.encode(
        {
            "iss": "myauthserver.com",
            "iat": now,
            "exp": now + datetime.timedelta(hours=1),
        },
        private_key,
        algorithm="RS256",
    )


def validate_access_token(access_token, cookie_fingerprint, public_key):
    try:
        payload = jwt.decode(access_token, public_key, algorithms=["RS256"])
        payload_fingerprint = payload.get("fingerprint")
        cookie_fingerprint = cookie_fingerprint
        if payload_fingerprint and cookie_fingerprint:
            fingerprint = base64.urlsafe_b64decode(cookie_fingerprint)
            is_valid = hashlib.sha256(fingerprint).digest() == base64.urlsafe_b64decode(
                payload_fingerprint
            )
            if is_valid:
                return True
    except jwt.exceptions.ExpiredSignatureError:
        return False
    except jwt.exceptions.DecodeError:
        pass

    return None
