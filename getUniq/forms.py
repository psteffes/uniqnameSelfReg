from django import forms
from django.core.validators import RegexValidator
from django.conf import settings

import datetime

class AcceptForm(forms.Form):
    accept = forms.BooleanField(
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
        validators=[RegexValidator(r'^\d{8,8}$', 'Enter a valid UMID.')],
    )

    email = forms.EmailField(
        required=True,
        #validators=[EmailValidator()],
    )

    # Make sure birth_date is 01/01/1700 or later - PSOBOSIAM-1533
    def clean_birth_date(self):
        data = self.cleaned_data['birth_date']
        if data < datetime.date(1700, 1, 1):
            raise forms.ValidationError('Value must be 01/01/1700 or later.')
        return data


class UniqnameForm(forms.Form):
    uniqname = forms.CharField(
        required=True,
        validators=[RegexValidator(r'^[a-z]{3,8}$', 'Enter a valid uniqname.')],
    )


# Most validation done in utils.validate_passwords_final
class PasswordForm(forms.Form):
    password = forms.CharField(
        required=True,
        strip=False,
    )

    confirm_password = forms.CharField(
        required=True,
        strip=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("confirm_password")

        if password1 != password2:
            raise forms.ValidationError('Passwords do not meet requirements.')

