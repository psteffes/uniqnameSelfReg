from django.conf import settings

import requests
import json
import logging

logger = logging.getLogger(__name__)

# We expect form.cleaned_data to be passed
def idproof_form_data(form_cleaned_data):

    try:
        # IDProof Web Service requires mutual auth
        cert = (settings.IDPROOF_CERT, settings.IDPROOF_KEY)

        # Build payload with form data
        payload = {
            'first_name': form_cleaned_data['first_name'],
            'last_name': form_cleaned_data['last_name'],
            'birth_date': form_cleaned_data['birth_date'],
            'umid': form_cleaned_data['umid'],
            'email': form_cleaned_data['email'],
        }
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        logger.debug('post_url={} payload={} timeout={}'.format(settings.IDPROOF_URL, json.dumps(payload, default=str), settings.REQUESTS_TIMEOUT_SECONDS))

        # Make the request
        r = requests.post(
            settings.IDPROOF_URL,
            data=json.dumps(payload, default=str),
            headers=headers,
            cert=cert,
            timeout=settings.REQUESTS_TIMEOUT_SECONDS,
        )

        # We expect all responses to be json
        try:
            logger.debug('response={} json={}'.format(r, r.json()))
        except:    # pragma: no cover
            logger.warn('Unable to json_decode response={}'.format(r))
            raise

        # Return empty entry (false) for 404, otherwise raise an error
        if r.status_code == 404:
            return False
        elif r.status_code >= 500:    # pragma: no cover
            raise ValueError('500')

        r.raise_for_status()

    except requests.exceptions.HTTPError as e:    # pragma: no cover
        logger.error('HTTPError={}'.format(e))
        raise

    except Exception as e:    # pragma: no cover
        logger.error('BaseException={}'.format(e))
        raise

    return r.json()

