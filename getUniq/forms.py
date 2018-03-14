from django import forms
from django.core.validators import RegexValidator, validate_email
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


class RecoveryForm(forms.Form):

    recovery = forms.EmailField(
        required=False,
    )

    confirmrecovery = forms.EmailField(
        required=False,
    )

    sms = forms.CharField(
        required=False,
    )

    confirmsms = forms.CharField(
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        recovery1 = cleaned_data.get("recovery")
        recovery2 = cleaned_data.get("confirmrecovery")
        sms1 = cleaned_data.get("sms")
        sms2 = cleaned_data.get("confirmsms")

        # Validate email address if given

        if recovery1 != recovery2:
            raise forms.ValidationError('Email addresses do not match')

        if recovery1 != "":
            validate_email(recovery1) # will raise forms.ValidationError if the address is invalid
            # Email validation already assures us of one and only one @ in the cleaned data
            full_domain = recovery1.split('@')[1]
            domain_parts = full_domain.split('.')
            registered_domain = domain_parts[-2] + '.' + domain_parts[-1]
            blacklist = settings.RECOVERY_EMAIL_DISALLOWED_DOMAINS
            if registered_domain in blacklist:
                raise forms.ValidationError(registered_domain+' email addresses are not allowed for password recovery')

        # Validate SMS if given

        # remove non-digits
        sms1=''.join(i for i in sms1 if i.isdigit())
        sms2=''.join(i for i in sms2 if i.isdigit())

        # ***
        cleaned_data["sms"] = sms1
        cleaned_data["confirmsms"] = sms2
        # ***

        if sms1 != sms2:
            raise forms.ValidationError('SMS phone numbers do not match')

        if sms1 != "":
            if len(sms1) != 10:
                raise forms.ValidationError('SMS phone number must be 10 digits')

