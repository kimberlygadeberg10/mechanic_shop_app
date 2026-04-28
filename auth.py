from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import jsonify, request
from jose import JWTError, jwt


SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"


def encode_token(customer_id):
    payload = {
        "customer_id": customer_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def token_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Authorization header missing or invalid."}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            customer_id = payload["customer_id"]
        except JWTError:
            return jsonify({"message": "Invalid or expired token."}), 401

        return route_function(customer_id, *args, **kwargs)

    return decorated_function
