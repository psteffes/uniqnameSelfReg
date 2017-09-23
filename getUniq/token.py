from django.conf import settings
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer

#import logging

#logger = logging.getLogger(__name__)


# Switch to JSONWebSignatures?

def generate_confirmation_token(data):
    #serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    serializer = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY,
        expires_in = settings.TOKEN_EXPIRATION_SECONDS,
    )
    return serializer.dumps(data, salt=settings.SECURITY_CONFIRM_SALT)


#def confirm_token(token):
#    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
def confirm_token(token):
    serializer = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY,
        expires_in = settings.TOKEN_EXPIRATION_SECONDS,
    )
    try:
        print('token={}'.format(token))
        #print('expiration={}'.format(expiration))
        data = serializer.loads(
            token,
            salt=settings.SECURITY_CONFIRM_SALT,
#            max_age=settings.TOKEN_EXPIRATION_SECONDS,
        )
    except Exception as e:
        print('e={}'.format(e))
        raise
    return data

