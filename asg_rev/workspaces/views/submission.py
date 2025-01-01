from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from workspaces.models import (
    Assignment, 
    Submission,
)
from workspaces.serializers.submission import (
    SubmissionRevieweeSerializer,
    SubmissionReviewerSerializer,
)
from workspaces.serializers.iteration import (
    IterationRevieweeSerializer,
) 
from workspaces.permissions import (
    IsWorkspaceMember,
    IsWorkspaceOwnerOrAdmin,
    IsChannelMember,
    IsReviewer, 
    IsReviewee,
)

class SubmissionRevieweeView(APIView):
    permission_classes = [
        (IsWorkspaceMember & IsReviewee) |
        IsWorkspaceOwnerOrAdmin
    ]

    def get_assignment(self):
        channel_pk = self.kwargs.get('channel_pk')
        return get_object_or_404(Assignment, id=channel_pk)

    def get(self, request, *args, **kwargs):
        assignment = self.get_assignment()
        submissions = Submission.objects.filter(
            sender=request.user, 
            assignment=assignment
        )
        serializer = SubmissionRevieweeSerializer(submissions, many=True)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )

    def post(self, request,*args, **kwargs):
        assignment = self.get_assignment()
        serializer = SubmissionRevieweeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                sender=request.user, 
                assignment=assignment
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request , *args, **kwargs):
        assignment = self.get_assignment()

        submission = Submission.objects.filter(
            sender=request.user, 
            assignment=assignment
        ).latest('submitted_at')

        serializer = SubmissionRevieweeSerializer(
            submission, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        assignment = self.get_assignment()

        try:
            submission = Submission.objects.filter(
                sender=request.user, 
                assignment=assignment
            ).latest('submitted_at')
        except Submission.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        submission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubmissionReviewerView(APIView):
    permission_classes = [
        (IsWorkspaceMember & IsReviewer) | IsWorkspaceOwnerOrAdmin
    ]

    def get_assignment(self):
        channel_pk = self.kwargs.get('channel_pk')
        return get_object_or_404(
            Assignment, 
            id=channel_pk
        )

    def get_submissions(self, assignment, user_id=None):
        if user_id:
            return Submission.objects.filter(
                sender=user_id, 
                assignment=assignment
            )
        return Submission.objects.filter(assignment=assignment)

    def get(self, request, *args, **kwargs):
        assignment = self.get_assignment()
        user_id = kwargs.get('user_id')

        submissions = self.get_submissions(
            assignment, 
            user_id=user_id
        )
        serializer = SubmissionReviewerSerializer(submissions, many=True)
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
