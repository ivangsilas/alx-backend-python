from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class (optional override for future custom behavior).
    """
    def authenticate(self, request):
        # You can extend or log here if needed
        return super().authenticate(request)
