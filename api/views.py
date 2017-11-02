from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TokenSerializer, SuggestionSerializer, UniqnameSerializer, PasswordSerializer
from getUniq.token import generate_confirmation_token
from getUniq import uniqname_services

import requests
import json
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def activation_link(request):
    """Return a user specific link to create or reactivate a uniqname"""
    logger.info('<RESTRequest: {} \'{}\' data={}>'.format(request.method, request.path, request.data))
    serializer = TokenSerializer(data=request.data)

    if serializer.is_valid():
        token = generate_confirmation_token({'umid': serializer['umid'].value})
        activation_link = request.build_absolute_uri(reverse('create', args=[token]))
        response = Response({
            "activation_link": activation_link,
            "expiration": settings.TOKEN_EXPIRATION_SECONDS
        })
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    logger.info('response.status_code={} response.data={}'.format(response.status_code, response.data))
    return response


@api_view(['POST'])
def get_suggestions(request):
    """Call uniqname services suggestions"""
    logger.info('<RESTRequest: {} \'{}\' data={}>'.format(request.method, request.path, request.data))
    serializer = SuggestionSerializer(data=request.data)

    if serializer.is_valid():
        suggestions = uniqname_services.get_suggestions(serializer['dn'].value, serializer['name_parts'].value)
        response = Response({"suggestions": suggestions})
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    logger.info('response.status_code={} response.data={}'.format(response.status_code, response.data))
    return response


@api_view(['POST'])
def find_uniqname(request):
    """Call uniqname services find"""
    logger.info('<RESTRequest: {} \'{}\' data={}>'.format(request.method, request.path, request.data))
    serializer = UniqnameSerializer(data=request.data)

    if serializer.is_valid():
        uid = uniqname_services.find_uniqname(serializer['uid'].value)
        response = Response({"uid": uid})
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    logger.info('response.status_code={} response.data={}'.format(response.status_code, response.data))
    return response


@api_view(['POST'])
def validate_password(request):
    """Call pwm password validation api"""
    logger.info('<RESTRequest: {} \'{}\'>'.format(request.method, request.path))
    serializer = PasswordSerializer(data=request.data)

    if serializer.is_valid():
        payload = {
            'showDetails': 'on',
            'uid': serializer['uid'].value,
            'password1': serializer['password1'].value,
            'password2': serializer['password2'].value,
        }
        logger.debug('post_url={} timeout={}'.format(settings.PASSWORD_VALIDATION_URL_BASE, settings.REQUESTS_TIMEOUT_SECONDS))    # Do not log payload
        r = requests.post(
            settings.PASSWORD_VALIDATION_URL_BASE,
            data=payload,
            timeout=settings.REQUESTS_TIMEOUT_SECONDS,
        )
        r_json = r.json()
        # Do not return password in the response to the browser
        try:
            del r_json['password2']
        except:    # pragma: no cover
            pass
        response = Response(r_json)
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Response json is very chatty so we are not logging it
    logger.info('response.status_code={}'.format(response.status_code))
    return response

