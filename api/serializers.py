from rest_framework import serializers
from django.core.validators import RegexValidator

class TokenSerializer(serializers.Serializer):
    identity_dn = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class SuggestionSerializer(serializers.Serializer):
    dn = serializers.CharField(required=False)
    name_parts = serializers.ListField(
        required=True,
        child = serializers.CharField(),
    )


class UniqnameSerializer(serializers.Serializer):
    uid = serializers.CharField(
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]{3,8}$', 'Enter a valid uniqname')],
    )


class PasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=False)
