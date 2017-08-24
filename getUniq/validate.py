
from ldap3 import Server, Connection, ALL

#import logging

#logger = logging.getLogger(__name__)

def validate_form_data(verify_form):

    try:

        # just fake it for now
        entry = {
            'umichRegDisplayGivenName': 'mega',
            'umichRegDisplaySurname': 'man',
            'umichRegUid': 'megaman',
            'umichRegEntityID': '13371337',
            'umichDirectoryID': '999-999-13379999999999999-999',
            'umichOudDacID': '0011223344',
            'umichOudPrefEmailAddress': 'megaman@gmail.com',
        }

        if entry['umichRegDisplaySurname'].lower() != verify_form.cleaned_data['last_name'].lower():
            raise Exception('last name does not match!')

        if entry['umichRegDisplayGivenName'].lower() != verify_form.cleaned_data['first_name'].lower():
            raise Exception('first name does not match!')

    except Exception as e:
        #logger.warn('Unable to validate identity - {} '.format(e))
        print('Unable to validate identity - {} '.format(e))
        return False

    #logger.info('form data has successfully validated')
    print('form data has successfully validated')
    return entry
