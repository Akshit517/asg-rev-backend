from workspaces.models.workspace import Workspace
from workspaces.models import (
    Category, 
    CategoryRole,
)
from workspaces.permissions import (
    IsWorkspaceMember, 
    IsWorkspaceOwnerOrAdmin,
)
from workspaces.serializers import (
    CategorySerializer,
    CategoryRoleSerializer,
)
from users.models import (
    User,
)

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        workspace_id = self.kwargs.get('workspace_pk')

        workspace = get_object_or_404(Workspace, id=workspace_id)

        if not CategoryRole.objects.filter(user=user, category__workspace=workspace).exists():
            return Category.objects.none()

        category_ids = CategoryRole.objects.filter(
                user=user, 
                category__workspace=workspace
            ).values_list('category', flat=True)

        return Category.objects.filter(id__in=category_ids)

    def perform_create(self, serializer):
        workspace_id = self.kwargs.get('workspace_id')
        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            raise ValidationError({"detail": "Workspace does not exist"})
        
        serializer.save(workspace=workspace)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy','add_member']:
            permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated, IsWorkspaceMember]
        
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['POST'])
    def add_member(self, request, pk=None, workspace_pk=None):
        try:
            category = self.get_object()

            user_id = request.data.get('user_id')
            role = request.data.get('role', 'category_member')

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {'detail': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            category_role, created = CategoryRole.objects.get_or_create(
                user=user,
                category=category,
                defaults={'role': role}
            )

            if not created:
                category_role.role = role
                category_role.save()

            serializer = CategoryRoleSerializer(category_role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Category.DoesNotExist:
            return Response(
                {'detail': 'Category not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
