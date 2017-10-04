from django.conf import settings
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer
import logging

logger = logging.getLogger(__name__)


def generate_confirmation_token(data):
    """
    Generate a JSONWebSignature. Used to send to the user to confirm email address
    """
    serializer = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY,
        expires_in = settings.TOKEN_EXPIRATION_SECONDS,
    )
    return serializer.dumps(data, salt=settings.SECURITY_CONFIRM_SALT)


def confirm_token(token):
    """
    Validate a JSONWebSignature. Return the json data
    """
    try:
        serializer = TimedJSONWebSignatureSerializer(
            settings.SECRET_KEY,
            expires_in = settings.TOKEN_EXPIRATION_SECONDS,
        )
        data = serializer.loads(
            token,
            salt=settings.SECURITY_CONFIRM_SALT,
        )
    except Exception as e:
        logger.error('e={}'.format(e))
        raise

    return data

