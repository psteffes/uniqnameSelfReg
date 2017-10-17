from rest_framework import serializers
from django.core.validators import RegexValidator

class TokenSerializer(serializers.Serializer):
    umid = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^[0-9]{8}$', 'Enter a valid UMID.')],
    )


class SuggestionSerializer(serializers.Serializer):
    dn = serializers.CharField(required=False)
    name_parts = serializers.ListField(
        required=True,
        child = serializers.CharField(),
    )


class UniqnameSerializer(serializers.Serializer):
    uid = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]{3,8}$', 'Enter a valid uniqname.')],
    )


class PasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]{3,8}$', 'Enter a valid uniqname.')],
    )
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=False)
