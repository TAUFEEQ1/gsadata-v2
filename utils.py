# signed_url_handler.py

from flask import current_app
import itsdangerous
from werkzeug.exceptions import NotFound

def generate_signed_url(entity_name):
    """
    Generates a signed URL for a given entity ID.
    """
    serializer = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(entity_name, salt='entity-salt')

def validate_signed_url(signed_url):
    """
    Validates the signed URL and retrieves the associated entity ID.
    If the URL is invalid or expired, raises a NotFound exception.
    """
    try:
        # Decode the signed URL token
        serializer = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
         # Set expiry time to 30 days (in seconds)
        expires_in = 60 * 60 * 24 * 30  # 30 days
        # expires_in = 1 * 60 # 1 minute for testing
        entity_name = serializer.loads(signed_url, salt='entity-salt', max_age=expires_in)  # Specify salt and max_age for validation
        return entity_name
    except (itsdangerous.SignatureExpired, itsdangerous.BadSignature):
        raise NotFound("Invalid or expired signed URL.")
