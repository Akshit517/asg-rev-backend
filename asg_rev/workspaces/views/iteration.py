from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from workspaces.models import (
    Submission,
)
from workspaces.permissions import (
    IsWorkspaceMember, 
    IsReviewer,
)
from workspaces.serializers import (
    IterationSerializer,
)

class IterationCreateView(APIView):
    permission_classes = [
        IsWorkspaceMember & IsReviewer
    ]

    def post(self, request, submission_id, *args, **kwargs):
        submission = get_object_or_404(Submission, id=submission_id)

        serializer = IterationSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(submission=submission)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
