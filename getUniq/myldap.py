from django.conf import settings

import ldap3
from ldap3 import Server, Connection, ALL
#import logging

#logger = logging.getLogger(__name__)

# Search the mcomm identities branch on UMID
def mcomm_reg_umid_search(umid):
    try:
        server = Server(settings.LDAP_URI)
        conn = Connection(server, settings.LDAP_USERNAME, settings.LDAP_PW, auto_bind=True)
        conn.search(
            'ou=Identities,o=Registry',
            '(umichRegEntityID={})'.format(umid),
            attributes=['*'],
        )

        # TODO: check for more than one result returned
        entry = conn.entries[0]
        print('entry={}'.format(entry))

    except Exception as e:
        print('error={}'.format(e))
        raise

    return entry
