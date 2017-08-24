from django.conf import settings
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from urllib.parse import quote_plus

import requests
import json
import base64
#import logging

#logger = logging.getLogger(__name__)

def oaep_encode(data):
    byte_data = json.dumps(data).encode('utf-8')

    with open('certs/mcuniqclient.pem', mode='rb') as publicfile:
        keydata = publicfile.read()
    pubkey = RSA.importKey(keydata)

    cipher_oaep = PKCS1_OAEP.new(pubkey)
    oaep_data = cipher_oaep.encrypt(byte_data)
    oaep_b64 = base64.b64encode(oaep_data)
    oaep_encoded = quote_plus(oaep_b64)

    return oaep_encoded


def make_post_request(url, payload):
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json',
        'Certificate': settings.UNIQNAME_SERVICES_CLIENT_CERT,
    }
    return requests.post(
        url,
        data=json.dumps(payload),
        headers=headers,
        timeout=settings.REQUESTS_TIMEOUT_SECONDS,
    )


def get_suggestions(dn, name_parts):

    try:
        print('dn={}'.format(dn))
        print('name_parts={}'.format(name_parts))

        data = {
            'dn': dn,
            'nameParts': name_parts,
        }

        print('data={}'.format(json.dumps(data)))

        oaep_encoded = oaep_encode(data)

        payload = {
            'name': 'suggestions',
            'coded': oaep_encoded,
        }

        r = make_post_request('https://uniqnameservices-dev.dsc.umich.edu:8443/uniqnameservices-v2/suggestions', payload)

        # We expect all responses to be json
        try:
            print('response={} json={}'.format(r, r.json()))
            print('suggestions={}'.format(r.json()['suggestions']))
            for name in r.json()['suggestions']:
                print('name={}'.format(name))
        except:
            print('Unable to json_decode response={}'.format(r))
            raise

    except Exception as e:
        #logger.warn('Unable to validate identity - {} '.format(e))
        print('get_suggestions error - {} '.format(e))
        raise

    #logger.info('form data has successfully validated')
    return r.json()['suggestions']


def find_uniqname(uid):
    try:
        data = {
            'uid': uid,
        }

        print('data={}'.format(json.dumps(data)))
        
        oaep_encoded = oaep_encode(data)

        payload = {
            'name': 'find',
            'coded': oaep_encoded,
        }

        r = make_post_request('https://uniqnameservices-dev.dsc.umich.edu:8443/uniqnameservices-v2/find', payload)

        try:
            print('response={} json={}'.format(r, r.json()))
        except:
            print('Unable to json_decode response={}'.format(r))
            raise

    except Exception as e:
        print('find error - {}'.format(e))
        raise

    return r.json()['uid']


def uniqname_create(dn, uid, umid, source):
    try:
        print('dn={}'.format(dn))
        print('uid={}'.format(uid))
        print('umid={}'.format(umid))
        print('source={}'.format(source))

        data = {
            'dn': dn,
            'uid': uid,
            'umid': umid,
            'source': source,
        }

        print('data={}'.format(json.dumps(data)))

        oaep_encoded = oaep_encode(data)

    except Exception as e:
        #logger.warn('Unable to validate identity - {} '.format(e))
        print('create error - {} '.format(e))
        return False

    #logger.info('form data has successfully validated')
    return True
