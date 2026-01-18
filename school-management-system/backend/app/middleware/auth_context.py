from flask import request, g
from app.core.jwt_utils import decode_token
from app.extensions import db
from app.models.users import UserAccount


def load_user_context():
    """
    Runs before every request.
    Decodes JWT once and stores minimal user context in flask.g
    """

    # Reset context
    g.current_user_id = None
    g.current_account_status = None
    g.current_user_role = None

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return

    token = auth_header.split(" ", 1)[1]

    try:
        payload = decode_token(token)
    except Exception:
        return

    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError):
        return

    user = (
        db.session.query(UserAccount)
        .filter_by(id=user_id)
        .first()
    )

    if not user:
        return

    # Store ONLY authoritative state
    g.current_user_id = user.id
    g.current_account_status = user.account_status
    g.current_user_role = user.role.name
