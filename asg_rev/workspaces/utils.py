from users.models import User
from crum import get_current_user

def get_current_user_or_none():
    u = get_current_user()
    if not isinstance(u, User):
        return None
    return u