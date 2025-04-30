# signed_url_handler.py

from flask import current_app
import itsdangerous
from werkzeug.exceptions import NotFound

def generate_signed_url(entity_name):
    """
    Generates a signed URL for a given entity ID.
    """
    serializer = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(entity_name)

def validate_signed_url(signed_url):
    """
    Validates the signed URL and retrieves the associated entity ID.
    If the URL is invalid or expired, raises a NotFound exception.
    """
    try:
        # Decode the signed URL token
        serializer = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        entity_name = serializer.loads(signed_url)  # No need to specify max_age here
        return entity_name
    except (itsdangerous.SignatureExpired, itsdangerous.BadSignature):
        raise NotFound("Invalid or expired signed URL.")
