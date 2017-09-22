from django import forms
from django.core.validators import RegexValidator


class TermsForm(forms.Form):
    i_agree = forms.BooleanField(
        required=True
    )


class VerifyForm(forms.Form):
    first_name = forms.CharField(
        required=True,
    )

    last_name = forms.CharField(
        required=True,
    )

    birth_date = forms.DateField(
        required=True,
    )

    umid = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^\d{8,8}$', 'Enter a valid UMID')],
    )

    email = forms.EmailField(
        required=True,
    )


class TokenForm(forms.Form):
    token = forms.CharField(
        required=True,
    )


class UniqnameForm(forms.Form):
    uniqname = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^[a-zA-Z]{3,8}$', 'Enter a valid uniqname')],
    )


class ReactivateForm(forms.Form):
    reactivate = forms.BooleanField(
        required=True,
    )


class PasswordForm(forms.Form):
    password = forms.CharField(
        required=True,
    )

    confirm_password = forms.CharField(
        required=True,
    )
