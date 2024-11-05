import cgi
from io import BytesIO
from django.http import JsonResponse
from users.models import User

class UserExistenceCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/register/':

            content_type = request.META.get('CONTENT_TYPE')
            if content_type and 'multipart/form-data' in content_type:
                # Boundary extraction
                boundary = content_type.split("boundary=")[-1].encode()
                form_data = BytesIO(request.body)
                
                # Parse the form data
                form = cgi.FieldStorage(fp=form_data, headers={'content-type': content_type}, environ={'REQUEST_METHOD': 'POST'})

                username = form.getvalue('username')
                email = form.getvalue('email')

                if email and User.objects.filter(email=email).exists():
                    return JsonResponse({"detail": "Email already exists."}, status=409)

                if username and User.objects.filter(username=username).exists():
                    return JsonResponse({"detail": "Username already exists."}, status=409)

        response = self.get_response(request)
        return response
