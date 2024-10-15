from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from workspaces.models.workspace import Workspace
from workspaces.models import (
    Category, 
    CategoryRole,
    ChannelRole
)
from workspaces.permissions import (
    IsWorkspaceMember, 
    IsWorkspaceOwnerOrAdmin,
)
from workspaces.serializers import (
    CategorySerializer,
    CategoryRoleSerializer,
)
from workspaces import utils

from django.shortcuts import get_object_or_404

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer

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
        workspace_id = self.kwargs.get('workspace_pk')
        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            raise ValidationError({"detail": "Workspace does not exist"})
        
        serializer.save(workspace=workspace)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy','add_or_update_member']:
            permission_classes = [IsWorkspaceOwnerOrAdmin]
        else:
            permission_classes = [IsWorkspaceMember]
        
        return [permission() for permission in permission_classes]

class CategoryMemberView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST','DELETE']:
            permission_classes = [IsWorkspaceOwnerOrAdmin]
        else:
            permission_classes = [IsWorkspaceMember]
        return [permission() for permission in permission_classes]

    def get(self, request, workspace_pk, category_pk):
        members = CategoryRole.objects.filter(category_id=category_pk)
        serializer = CategoryRoleSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, workspace_pk, category_pk):
        category = get_object_or_404(Category, pk=category_pk)
        
        user_email = request.data.get('user_email')
        role = request.data.get('role', 'category_member')

        if not user_email:
            return Response(
                {"detail": "User email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, exists = utils.check_user_exists_and_workspace_member(
            email=user_email,
            workspace_id=workspace_pk
            )
        if not exists:
            return Response(
                {"detail": "User does not exist or is not a workspace member."},
                status=status.HTTP_404_NOT_FOUND
            )

        category_role, created = CategoryRole.objects.update_or_create(
            user=user,
            category=category,
            defaults={'role': role}
        )

        serializer = CategoryRoleSerializer(category_role)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def delete(self, request, workspace_pk, category_pk):
        email = request.data.get('user_email')
        if not email:
            return Response(
                {"detail": "Email query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif request.user.email == email:
            return Response(
                {"detail": "You cannot remove yourself from the workspace."},
                status=status.HTTP_403_FORBIDDEN
            )

        user, exists = utils.check_user_exists_and_workspace_member(
            email=email,
            workspace_id=workspace_pk
            )
        if not exists:
            return Response(
                {"detail": "User does not exist or is not a workspace member."},
                status=status.HTTP_404_NOT_FOUND
            )
        member = get_object_or_404(
            CategoryRole, 
            user=user, category_id=category_pk
        )
        member.delete()

        ChannelRole.objects.filter(
            user=user, 
            channel__category_id=category_pk
        ).delete()
        
        return Response(
            {"detail": "Member has been removed from the category."},
            status=status.HTTP_204_NO_CONTENT
        )

class CategoryMemberDetailView(APIView):
    permission_classes = [IsWorkspaceMember]

    def get(self, request, workspace_pk, category_pk):
        email = request.query_params.get('email')
        if not email:
            return Response(
                {"detail": "Email query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, exists = utils.check_user_exists_and_workspace_member(
            email=email,
            workspace_id=workspace_pk
            )
        if not exists:
            return Response(
                {"detail": "User does not exist or is not a workspace member."},
                status=status.HTTP_404_NOT_FOUND
            )
        member = get_object_or_404(CategoryRole, user=user, category_id=category_pk)

        serializer = CategoryRoleSerializer(member)
        return Response(serializer.data)
