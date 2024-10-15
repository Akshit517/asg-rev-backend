from rest_framework.permissions import BasePermission


class IsCategoryAdmin(BasePermission):
    '''not implemented'''
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.category_role.filter(
            user=request.user, 
            role='category_admin'
        ).exists()

class IsCategoryMember(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.category_role.filter(
            role__startswith='category_'
        ).exists()
