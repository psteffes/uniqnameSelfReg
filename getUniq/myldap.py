from django.conf import settings

import ldap3
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
#import logging

#logger = logging.getLogger(__name__)

# Search the mcomm identities branch on UMID
def mcomm_reg_umid_search(umid):
    try:
        print('searching for umichRegEntityID={}'.format(umid))
        server = Server(settings.LDAP_URI)
        conn = Connection(server, settings.LDAP_USERNAME, settings.LDAP_PW, auto_bind=True)
        conn.search(
            'ou=Identities,o=Registry',
            '(umichRegEntityID={})'.format(umid),
            attributes=['*'],
            time_limit=settings.LDAP_TIME_LIMIT,
        )

        # TODO: check for more than one result returned
        entry = ''
        print('len(conn.entries)={}'.format(len(conn.entries)))
        if len(conn.entries) == 1:
            entry = conn.entries[0]
            print('entry={}'.format(entry))

    except Exception as e:
        print('error={}'.format(e))
        raise

    return entry


def set_status_complete(dn):
    try:
        server = Server(settings.LDAP_URI)
        conn = Connection(server, settings.LDAP_USERNAME, settings.LDAP_PW, auto_bind=True)

        mod_attrs = {
            'umichGetUniqStatus': [(MODIFY_REPLACE, ['COMPLETE'])],
        }
        result = conn.modify(dn, mod_attrs)

        if conn.modify(dn, mod_attrs):
            print('Successfully set umichGetUniqStatus=COMPLETE for dn={}'.format(dn))
        else:
            print('Error updating umichGetUniqStatus for dn={}, details={}'.format(dn, conn.result))

    except Exception as e:
        print('error={}'.format(e))
        raise

    return
