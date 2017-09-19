from django.conf import settings
from itsdangerous import URLSafeTimedSerializer

#import logging

#logger = logging.getLogger(__name__)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt=settings.SECURITY_CONFIRM_SALT)


def confirm_token(token, expiration=settings.TOKEN_EXPIRATION_LENGTH):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        print('token={}'.format(token))
        print('expiration={}'.format(expiration))
        email = serializer.loads(
            token,
            salt=settings.SECURITY_CONFIRM_SALT,
            max_age=expiration,
        )
    except Exception as e:
        print('e={}'.format(e))
        raise
    return email

