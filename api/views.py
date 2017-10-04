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

    logger.info('Return status_code={} response={}'.format(response.status_code, response.data))
    return response


@api_view(['POST'])
def get_suggestions(request):
    """Call uniqname services suggestions"""
    logger.info('<RESTRequest: {} \'{}\' data={}>'.format(request.method, request.path, request.data))
    logger.info(dir(request))
    serializer = SuggestionSerializer(data=request.data)

    if serializer.is_valid():
        suggestions = uniqname_services.get_suggestions(serializer['dn'].value, serializer['name_parts'].value)
        response = Response({"suggestions": suggestions})
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    logger.info('Return status_code={} response={}'.format(response.status_code, response.data))
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

    logger.info('Return status_code={} response={}'.format(response.status_code, response.data))
    return response


@api_view(['GET'])
def validate_password(request):
    """Call password validation api"""
    logger.info('<RESTRequest: {} \'{}\'>'.format(request.method, request.path))
    serializer = PasswordSerializer(data=request.GET)

    if serializer.is_valid():
        r = requests.get(
            '{}&uid={}&password1={}&password2={}'.format(settings.PASSWORD_VALIDATION_URL_BASE, serializer['uid'].value, serializer['password1'].value, serializer['password2'].value),
        )
        response = Response(r.json())
    else:
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    logger.info('Return status_code={} response={}'.format(response.status_code, response.data))
    return response

