from flask import request, g
from app.core.jwt_utils import decode_token

def load_user_context():
    """
    Runs before every request.
    Decodes JWT once and stores user info in flask.g
    """
    g.current_user_id = None
    g.token_payload = None

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return

    token = auth_header.split(" ", 1)[1]

    try:
        payload = decode_token(token)
    except Exception:
        return

    g.token_payload = payload
    g.current_user_id = int(payload["sub"])
