from django.conf import settings
import requests

#import logging

#logger = logging.getLogger(__name__)

# Validate an entry is eligible based on the umichGetUniqname ObjectClass
def getuniq_eligible(entry):

    try:
        eligible = False
        print('umichgetuniqstatus={}'.format(entry['umichGetUniqStatus']))
        if entry['umichGetUniqStatus'][0] == 'ELIGIBLE' and entry['umichGetUniqEntitlingRoles'][0] != '':
            eligible = True

    except Exception as e:
        pass

    return eligible


def validate_passwords(uid, password1, password2):

    try:
        valid = False
        r = requests.get(
            '{}&uid={}&password1={}&password2={}'.format(settings.PASSWORD_VALIDATION_URL_BASE, 'uid', password1, password2),
        )

        if r.json()['evaluation']['valid'] == True:
            valid = True

    except Exception as e:
        pass

    return valid
