from rest_framework.response import Response
from rest_framework import status
from users.models import User
from crum import get_current_user

def get_current_user_or_none():
    u = get_current_user()
    if not isinstance(u, User):
        return None
    return u

def check_user_exists_and_workspace_member(*, email: str, workspace_id: str):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None, False 
    
    is_member = user.workspace_role.filter(workspace_id=workspace_id).exists()
    return user, is_member
