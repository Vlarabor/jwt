from flask import Flask, request, jsonify, make_response
import datetime
import base64

from auth import (
    generate_access_token,
    generate_fingerprint,
    generate_refresh_token,
    validate_access_token,
    validate_user_login,
)
from rsa import load_keys

PRIVATE_KEY, PUBLIC_KEY = load_keys()


app = Flask(__name__)

# Handle CORS
@app.after_request
def after_request_func(response):
    origin = request.headers.get("Origin")
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Origin, X-Requested-With, Content-Type, Accept",
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "accessToken, refreshToken, authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, PATCH, DELETE"
        )
        if origin:
            response.headers.add("Access-Control-Allow-Origin", origin)
    else:
        response.headers.add("Access-Control-Allow-Credentials", "true")
        if origin:
            response.headers.add("Access-Control-Allow-Origin", origin)

    return response


@app.route("/token", methods=["GET", "POST"])
def token():
    if request.method == "POST":
        username = request.authorization.username
        password = request.authorization.password
        user, user_id = validate_user_login(username, password)
        if user:
            fingerprint, fingerprint_hash = generate_fingerprint()
            now = datetime.datetime.utcnow()
            access_token = generate_access_token(
                user_id=user_id,
                fingerprint_hash=fingerprint_hash,
                now=now,
                private_key=PRIVATE_KEY,
            )
            refresh_token = generate_refresh_token(
                fingerprint_hash=fingerprint_hash, now=now, private_key=PRIVATE_KEY
            )

            # Send access and refresh token in response body
            response = jsonify(
                {
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
                }
            )

            # Send fingerprint (base64url-encoded) as a http only cookie
            response.set_cookie(
                key="fingerprint",
                value=base64.urlsafe_b64encode(fingerprint).decode(),
                max_age=900,
                secure=False,  # only disabled for localhost
                httponly=True,
                samesite="lax",
            )
            return response
        else:
            return jsonify({"errors": "Invalid credentials"}), 401
    elif request.method == "GET":
        access_token = request.headers.get("accessToken")
        if access_token:
            is_valid = validate_access_token(
                access_token=access_token,
                cookie_fingerprint=request.cookies.get("fingerprint"),
                public_key=PUBLIC_KEY,
            )
        if is_valid is True:
            return jsonify({"msg": "Successfully authenticated!"})
        elif is_valid is False:
            return jsonify({"errors": "Expired token!"}), 400
        return (
            jsonify({"errors": "Invalid or missing access token or fingerprint"}),
            400,
        )


if __name__ == "__main__":
    app.run(debug=True)
