from django.conf import settings
import requests

def getuniq_eligible(entry):
    """Returns True if user is eligible to use this service"""
    try:
        eligible = False
        if entry['umichGetUniqStatus'][0] == 'ELIGIBLE' and entry['umichGetUniqEntitlingRoles'][0] != '':
            eligible = True

    except Exception as e:
        pass

    return eligible


def validate_passwords(uid, password1, password2):
    """Returns True if passwords are valid"""
    try:
        valid = False
        params = {
            'uid': uid,
            'password1': password1,
            'password2': password2,
        }
        r = requests.get(
            settings.PASSWORD_VALIDATION_URL_BASE,
            params=params, 
            timeout=settings.REQUESTS_TIMEOUT_SECONDS,
        )
        if r.json()['evaluation']['valid'] == True:
            valid = True

    except Exception as e:    # pragma: no cover
        pass

    return valid
