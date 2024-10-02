from rest_framework.permissions import BasePermission

class IsReviewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.channel_role.filter(
            user=request.user, 
            role='reviewer'
        ).exists()

class IsReviewee(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return obj.channel_role.filter(
            user=request.user, 
            role='reviewer'
        ).exists()
