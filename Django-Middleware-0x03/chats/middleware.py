# chats/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict
import threading
from django.http import HttpResponseForbidden


# Set up logger to write to requests.log
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 18:00 (6PM) and 21:00 (9PM)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is only allowed between 6PM and 9PM.")
        return self.get_response(request)

# middleware to bock offensive words


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(list)  # {ip: [timestamps]}
        self.lock = threading.Lock()

    def __call__(self, request):
        if request.path.startswith("/api/messages/") and request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            with self.lock:
                # Remove messages older than 1 minute
                self.message_log[ip] = [
                    timestamp for timestamp in self.message_log[ip]
                    if now - timestamp < timedelta(minutes=1)
                ]

                if len(self.message_log[ip]) >= 5:
                    return HttpResponseForbidden("Too many messages. Please wait before sending more.")

                self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Support for real IPs behind proxies if needed
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')




class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware if user is not authenticated
        if request.user.is_authenticated:
            protected_paths = [
                "/api/admin/",         # Admin dashboard or endpoints
                "/api/moderate/",      # Moderation endpoints
                "/api/manage-users/",  # Example paths that require role checking
            ]

            for path in protected_paths:
                if request.path.startswith(path):
                    user_role = getattr(request.user, 'role', None)
                    if user_role not in ['admin', 'moderator']:
                        return HttpResponseForbidden("Access denied: insufficient permissions.")
                    break  # Path matched and role verified

        return self.get_response(request)
