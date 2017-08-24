from django.shortcuts import render
from django.urls import reverse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TokenSerializer, SuggestionSerializer, UniqnameSerializer, PasswordSerializer
from getUniq.token import generate_confirmation_token
from getUniq import uniqname_services

import requests # test

@api_view(['POST'])
#def get_token(request, format=None):
def create_invitation_link(request):
    """
    Return a user specific link to create or reactivate a uniqname
    """
    serializer = TokenSerializer(data=request.data)
    print('serializer={}'.format(serializer))

    if serializer.is_valid():
        print('s.email={}'.format(serializer['identity_dn'].value))
        token = generate_confirmation_token(serializer['identity_dn'].value)
        print('token={}'.format(token))
        secure_url = request.build_absolute_uri(reverse('create', args=[token]))
        print('secure_url={}'.format(secure_url))
        return Response({"message": "Got some data!", "data": request.data, "secure_url": secure_url})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
def get_suggestions(request):
    """
    Call uniqname services suggestions
    """
    print(request)
    serializer = SuggestionSerializer(data=request.data)
    print('serializer={}'.format(serializer))

    if serializer.is_valid():
        print('s.values={}'.format(serializer['dn'].value))
        suggestions = uniqname_services.get_suggestions(serializer['dn'].value, serializer['name_parts'].value)
        return Response({"message": "Got some data!", "data": request.data, "suggestions": suggestions})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def find_uniqname(request):
    """
    Call uniqname services find
    """
    print(request)
    serializer = UniqnameSerializer(data=request.data)
    print('serializer={}'.format(serializer))

    if serializer.is_valid():
        print('data={}'.format(serializer.data))
        found = uniqname_services.find_uniqname(serializer['uid'].value)
        print('found={}'.format(found))
        return Response({"message": "Got some data!", "data": request.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def validate_password(request):
    """
    Call password validation api
    """
    print('request={}'.format(request))
    print('pw={}'.format(request.GET.get('password1')))
    serializer = PasswordSerializer(data=request.GET)
    print('serializer={}'.format(serializer))

    if serializer.is_valid():
        print('data={}'.format(serializer.data))
        r = requests.get(
            'https://pwm-dev.dsc.umich.edu/passwordValidation/scrutinizer.json?showDetails=on&uid=batman&password1={}&password2={}'.format(serializer['password1'].value, serializer['password2'].value),
        )
        return Response(r.json())
    else:
        print('something was not valid')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
