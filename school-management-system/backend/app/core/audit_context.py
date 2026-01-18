from typing import Optional
from contextvars import ContextVar

_current_user = ContextVar("current_user", default=None)

def set_current_user(user_id: Optional[int]):
    _current_user.set(user_id)

def get_current_user_id() -> Optional[int]:
    return _current_user.get()
