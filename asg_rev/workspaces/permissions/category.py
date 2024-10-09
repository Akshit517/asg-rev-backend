from rest_framework.permissions import BasePermission

'''not implemented'''

class IsCategoryAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.category_role.filter(
            user=request.user, 
            role='category_admin'
        ).exists()

class IsCategoryMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.category_role.filter(
            user=request.user, 
            role='category_member'
        ).exists()
