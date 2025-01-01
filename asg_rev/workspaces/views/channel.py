from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import User
from workspaces import utils
from workspaces.models import (
    Category,
    Channel, 
    ChannelRole,
    Assignment,
)
from workspaces.serializers import (
    ChannelSerializer, 
    AssignmentSerializer,
    ChannelRoleSerializer
)
from workspaces.permissions import (
    IsReviewer, 
    IsReviewee, 
    IsCategoryMember,
    IsChannelMember,
    IsWorkspaceOwnerOrAdmin,
    IsWorkspaceMember,
)

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer

    def get_queryset(self):
        user = self.request.user
        category_id = self.kwargs.get('category_pk')
        channel_ids = ChannelRole.objects.filter(user=user).values_list('channel', flat=True)
        return Channel.objects.filter(
            id__in=channel_ids,
            category_id=category_id
        )

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsWorkspaceOwnerOrAdmin | IsReviewer]
        elif self.action in ['list']:
            permission_classes = [ IsWorkspaceOwnerOrAdmin | IsCategoryMember ]
        elif  self.action in ['retrieve']:
            permission_classes = [ IsWorkspaceOwnerOrAdmin | IsChannelMember ]

        return [permission() for permission in permission_classes]

class ChannelMemberView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST','DELETE','PUT']:
            permission_classes = [IsWorkspaceOwnerOrAdmin | IsReviewer]
        else:  
            permission_classes = [IsWorkspaceOwnerOrAdmin | IsChannelMember]  
        return [permission() for permission in permission_classes]

    def get(self, request, workspace_pk, category_pk, channel_pk):
        queryset = ChannelRole.objects.filter(channel_id=channel_pk)
        email = request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(user__email=email)
        serializer = ChannelRoleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, workspace_pk, category_pk, channel_pk):
        channel = get_object_or_404(Channel, pk=channel_pk)
        
        email = request.data.get('user_email')
        role = request.data.get('role', 'reviewee')
        
        if not email:
            return Response(
                {"detail": "User email is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, email=email)
        if not user.workspace_role.filter(workspace_id=workspace_pk).exists():
            return Response(
                {"detail": "User is not a workspace member."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        channel_role, created = ChannelRole.objects.update_or_create(
            user=user, 
            channel=channel,
            defaults={'role': role}
        )

        serializer = ChannelRoleSerializer(channel_role)

        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def delete(self, request, workspace_pk, category_pk, channel_pk):
        email = request.data.get('user_email')
        if not email:
            return Response(
                {"detail": "User email is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        elif request.user.email == email:
            return Response(
                {"detail": "You cannot remove yourself from the workspace."},
                status=status.HTTP_403_FORBIDDEN
            )

        user = get_object_or_404(User, email=email)
        member = get_object_or_404(ChannelRole, user=user, channel_id=channel_pk)
        member.delete()

        return Response(
            {"detail": "Member has been removed from the channel."}, 
            status=status.HTTP_204_NO_CONTENT
        )

    def put(self, request, workspace_pk, category_pk, channel_pk):
        email = request.data.get('user_email')
        new_role = request.data.get('role')

        if not email:
            return Response(
                {"detail": "User email is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not new_role:
            return Response(
                {"detail": "New role is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, email=email)
        channel_role = get_object_or_404(
            ChannelRole, user=user, channel_id=channel_pk
        )

        channel_role.role = new_role
        channel_role.save()

        serializer = ChannelRoleSerializer(channel_role)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
