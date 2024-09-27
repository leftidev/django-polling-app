from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
import logging

# Set up logger
logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_admin_login(sender, request, user, **kwargs):
    if user.is_staff:  # This checks if the logged-in user is an admin
        logger.info(f"Admin {user.username} logged in.")
        print(f"Admin {user.username} logged in from {request.META.get('REMOTE_ADDR')}.")

@receiver(user_login_failed)
def log_admin_login_failed(sender, credentials, request, **kwargs):
    logger.warning(f"Failed login attempt for username: {credentials.get('username')}")
    print(f"Failed login attempt for username: {credentials.get('username')} from {request.META.get('REMOTE_ADDR')}.")
