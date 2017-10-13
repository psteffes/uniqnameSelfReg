from django.conf import settings
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from urllib.parse import quote_plus

import requests
import json
import base64
import logging

logger = logging.getLogger(__name__)

class UniqnameServicesError(Exception):
    """Exception raised if uniqname_services fails or errors"""

    def __init__(self, message):
        self.message = message


def oaep_encode(data):
    """Returns an oaep_encoded string"""
    byte_data = json.dumps(data).encode('utf-8')

    with open(settings.UNIQNAME_SERVICES_PUBKEY, mode='rb') as publicfile:
        keydata = publicfile.read()
    pubkey = RSA.importKey(keydata)

    cipher_oaep = PKCS1_OAEP.new(pubkey)
    oaep_data = cipher_oaep.encrypt(byte_data)
    oaep_b64 = base64.b64encode(oaep_data)
    oaep_encoded = quote_plus(oaep_b64)

    return oaep_encoded


def make_post_request(url, payload, timeout=settings.REQUESTS_TIMEOUT_SECONDS):
    """POST to the uniqname_services url. Return the response"""
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Certificate': settings.UNIQNAME_SERVICES_CLIENT_CERT,
    }
    logger.debug('timeout={}'.format(timeout))
    return requests.post(
        url,
        data=json.dumps(payload),
        headers=headers,
        timeout=timeout,
    )


def get_suggestions(dn, name_parts):
    """Returns suggestions given by uniqname_services suggestions endpoint"""
    try:
        data = {
            'dn': dn,     # dn does not seem to add any value to this call
            'nameParts': name_parts,
        }
        payload = {
            'name': 'suggestions',
            'coded': oaep_encode(data),
        }
        r = make_post_request('{}/suggestions'.format(settings.UNIQNAME_SERVICES_URL_BASE), payload)

        # We expect all responses to be json
        try:
            logger.info('response={} json={}'.format(r, r.json()))
        except:
            logger.error('Unable to json_decode response={}'.format(r))
            raise

    except Exception as e:
        logger.error('e={}'.format(e))
        raise

    return r.json()['suggestions']


def find_uniqname(uid):
    """Return uniqname given by uniqname_services find endpoint"""
    try:
        data = {
            'uid': uid,
        }
        payload = {
            'name': 'find',
            'coded': oaep_encode(data),
        }
        r = make_post_request('{}/find'.format(settings.UNIQNAME_SERVICES_URL_BASE), payload)

        # We expect all responses to be json
        try:
            logger.info('response={} json={}'.format(r, r.json()))
        except:
            logger.error('Unable to json_decode response={}'.format(r))
            raise

    except Exception as e:
        logger.error('e={}'.format(e))
        raise

    return r.json()['uid']


def create_uniqname(dn, uid, umid):
    """Call uniqname-services create endpoint"""
    try:
        data = {
            'dn': dn,
            'uid': uid,
            'umid': umid,
        }
        payload = {
            'name': 'create',
            'coded': oaep_encode(data),
        }
        r = make_post_request('{}/create'.format(settings.UNIQNAME_SERVICES_URL_BASE), payload, timeout=105)

        # We expect all responses to be json
        try:
            logger.info('response={} json={}'.format(r, r.json()))
        except:
            logger.error('Unable to json_decode response={}'.format(r))
            raise

        if r.json()['status'] != 'success':
            raise UniqnameServicesError('Uniqname create failed')

    except Exception as e:
        logger.error('e={}'.format(e))
        raise


def reactivate_uniqname(dn, umid):
    """Call uniqname-services reactivate endpoint"""
    try:
        data = {
            'dn': dn,
            'umid': umid,
        }
        payload = {
            'name': 'reactivate',
            'coded': oaep_encode(data),
        }
        r = make_post_request('{}/reactivate'.format(settings.UNIQNAME_SERVICES_URL_BASE), payload, timeout=105)

        # We expect all responses to be json
        try:
            logger.info('response={} json={}'.format(r, r.json()))
        except:
            logger.error('Unable to json_decode response={}'.format(r))
            raise

        if r.json()['status'] != 'success':
            raise UniqnameServicesError('Uniqname reactivation failed')

    except Exception as e:
        logger.error('e={}'.format(e))
        raise


def reset_password(uid, password):
    """Call uniqname-services passwordReset endpoint"""
    try:
        data = {
            'uid': uid,
            'password': password,
        }
        payload = {
            'name': 'passwordReset',
            'coded': oaep_encode(data),
        }
        r = make_post_request('{}/passwordReset'.format(settings.UNIQNAME_SERVICES_URL_BASE), payload)

        # We expect all responses to be json
        try:
            logger.info('response={} json={}'.format(r, r.json()))
        except:
            logger.error('Unable to json_decode resposne={}'.format(r))

        if r.json()['status'] != 'success':
            raise UniqnameServicesError('passwordReset failed')

    except Exception as e:
        logger.error('e={}'.format(e))
        raise

