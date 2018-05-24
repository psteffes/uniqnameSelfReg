from django.conf import settings
import logging
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

logger = logging.getLogger(__name__)

# Search the mcomm identities branch on UMID
def mcomm_reg_umid_search(umid):
    try:
        entry = ''
        logger.debug('Searching for umichRegEntityID={}'.format(umid))

        with Connection(
            Server(settings.LDAP_URI),
            settings.LDAP_USERNAME,
            settings.LDAP_PW,
            auto_bind=True,
        ) as conn:

            conn.search(
                'ou=Identities,o=Registry',
                '(umichRegEntityID={})'.format(umid),
                attributes=['*'],
                time_limit=settings.LDAP_TIME_LIMIT,
            )

            # TODO: check for more than one result returned
            if len(conn.entries) == 1:
                entry = conn.entries[0]
                logger.debug('Found dn={}'.format(entry.entry_dn))

    # Do not re-raise, treat an exception as entry not found
    except Exception as e:    # pragma: no cover
        logger.error('error={}'.format(e))

    return entry


def set_status_complete(dn):
    try:
        result = False

        with Connection(
            Server(settings.LDAP_URI),
            settings.LDAP_USERNAME,
            settings.LDAP_PW,
            auto_bind=True,
        ) as conn:

            mod_attrs = {
                'umichGetUniqStatus': [(MODIFY_REPLACE, ['COMPLETE'])],
            }
            result = conn.modify(dn, mod_attrs)

            # conn.modify returns True if successful
            if result:
                logger.info('Set umichGetUniqStatus=COMPLETE for dn={}'.format(dn))
            else:    # pragma: no cover
                logger.error('Error updating umichGetUniqStatus for dn={}, details={}'.format(dn, conn.result))

    # Do not re-raise, just fail silently for now
    except Exception as e:    # pragma: no cover
        logger.error('Unable to update umichGetUniqStatus, e={}'.format(e))

    return result
