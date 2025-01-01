from django.http import JsonResponse
from users.models import User
import json

class UserExistenceCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/register/':

            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            username = data.get('username')
            
            if email and User.objects.filter(email=email).exists():
                return JsonResponse({"detail": "Email already exists."}, status=409)

            if username and User.objects.filter(username=username).exists():
                return JsonResponse({"detail": "Username already exists."}, status=409)

        response = self.get_response(request)
        return response
