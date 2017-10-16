from django.conf import settings
import logging
import ldap3
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

logger = logging.getLogger(__name__)

# Search the mcomm identities branch on UMID
def mcomm_reg_umid_search(umid):
    try:
        logger.debug('searching for umichRegEntityID={}'.format(umid))
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
        if len(conn.entries) == 1:
            entry = conn.entries[0]

    except Exception as e:    # pragma: no cover
        logger.error('error={}'.format(e))
        raise

    return entry


def set_status_complete(dn):    # pragma: no cover
    try:
        server = Server(settings.LDAP_URI)
        conn = Connection(server, settings.LDAP_USERNAME, settings.LDAP_PW, auto_bind=True)

        mod_attrs = {
            'umichGetUniqStatus': [(MODIFY_REPLACE, ['COMPLETE'])],
        }
        result = conn.modify(dn, mod_attrs)

        if conn.modify(dn, mod_attrs):
            logger.info('Successfully set umichGetUniqStatus=COMPLETE for dn={}'.format(dn))
        else:
            logger.error('Error updating umichGetUniqStatus for dn={}, details={}'.format(dn, conn.result))

    except Exception as e:
        logger.error('error={}'.format(e))
        raise

    return
