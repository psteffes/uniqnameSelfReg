from django.conf import settings
from itsdangerous import URLSafeTimedSerializer

#import logging

#logger = logging.getLogger(__name__)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt=settings.SECURITY_CONFIRM_SALT)


def confirm_token(token, expiration=300):
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

#def generate_confirmation_token(email):
#    token = '123456'
#    return token


#def confirm_token(token):
#    print('token={}'.format(token))
#    if token != '123456':
#        return False
#
#    return True

