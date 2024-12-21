from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class UploadMediaView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    

    def post(self, request):
        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']
        try:
            file_path = default_storage.save(f'uploaded/{image.name}', ContentFile(image.read()))
            file_url = request.build_absolute_uri(f'/media/{file_path}')
            return Response({'url': file_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Failed to upload file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

