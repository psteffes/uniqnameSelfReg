from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib import messages

from .forms import AcceptForm, VerifyForm, TokenForm, UniqnameForm, PasswordForm
from .idproof import idproof_form_data 
from .token import generate_confirmation_token, confirm_token
from .uniqname_services import get_suggestions, create_uniqname, reactivate_uniqname, reset_password
from .utils import getuniq_eligible, validate_passwords
from .myldap import mcomm_reg_umid_search, set_status_complete

#test
import json

import logging

logger = logging.getLogger(__name__)


def terms(request):
    logger.info(request)
    logger.debug(request.session.items())

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = AcceptForm(request.POST)
        if form.is_valid():
            # Flush the session for a clean start
            request.session.flush()
            request.session['agreed_to_terms'] = True
            return redirect('verify')
        else:
            logger.warning('invalid AcceptForm')
    # On a GET or any other request method create a blank form
    else:
        form = AcceptForm()

    return render(request, 'terms.html', {'form': form})


def verify(request):
    logger.info(request)
    logger.debug(request.session.items())

    # Redirect the user to the terms page if they have not accepted them yet
    if not request.session.get('agreed_to_terms', False):    # False is the default
        logger.debug('User has not agreed to terms, redirect to terms')
        return redirect('terms')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VerifyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required)
            logger.debug('form={}'.format(form.cleaned_data))
            entry = idproof_form_data(form.cleaned_data)
            if entry:
                logger.debug('entry={}'.format(entry))

                # If the person is not eligible, tell them nicely
                if not getuniq_eligible(entry):
                    messages.error(request, settings.INELIGIBLE_ALERT_MSG)
                    logger.warn('User is not eligible, redirect to terms')
                    return redirect('terms')

                # Generate the token and build the secure link
                data = {
                    'umid': entry['umichRegEntityID'][0],
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                }
                token = generate_confirmation_token(data)
                secure_url = request.build_absolute_uri(reverse('create', args=[token]))
                logger.debug('secure_url={}'.format(secure_url))

                # Send an email to the user with the secure_url to continue
                plaintext = get_template('email.txt')
                html = get_template('email.html')
                d = {'secure_url': secure_url}
                subject = 'Please confirm your email'
                text_content = plaintext.render(d)
                html_content = html.render(d)
                email = form.cleaned_data['email']
                send_mail(
                    subject,
                    text_content,
                    '4help@umich.edu',
                    [email],
                    html_message=html_content,
                    fail_silently=False,
                )
                logger.info('Confirmation link successfully sent to {}'.format(email))

                # Update session and send them to confirm_email
                del request.session['agreed_to_terms']
                request.session['email'] = email 
                return redirect('confirm_email')
            # idVerification failed
            else:
                form.add_error(None, 'Unable to validate identity')
        # Form not valid
        else:
            logger.warning('form.errors={}'.format(form.errors.as_json(escape_html=False)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VerifyForm()

    return render(request, 'verify.html', {'form': form})


def confirm_email(request):
    logger.info(request)
    logger.debug(request.session.items())
    email = request.session.get('email', False)
    if email:
        context = {'email': email}
        #request.session.flush()
        return render(request, 'confirm_email.html', context)
    else:
        logger.warning('No email address for user, redirect to terms')
        return redirect('terms')


def create(request, token):
    logger.info(request)
    logger.debug(token)
    logger.debug(request.session.items())

    # Validate the token
    try:
        data = confirm_token(token)
        umid = data['umid']
        logger.debug('data={}'.format(data))
    except:
        logger.warning('Confirmation link is invalid or expired, redirect to terms')
        messages.error(request, 'The confirmation link is invalid or has expired, please verify your identity and try again.')
        return redirect('terms')

    # Go away if you've already created a uniqname
    has_uid = request.session.get('uid', False)
    if has_uid:
        logger.warning('User already has a uniqname, redirect to terms')
        return redirect('terms')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = UniqnameForm(request.POST)
        dn = request.session.get('dn', False)
        if form.is_valid() and dn and umid:
            logger.debug('form={}'.format(form.cleaned_data))
            create_uniqname(dn, form.cleaned_data['uniqname'], umid)
            request.session['uid'] = form.cleaned_data['uniqname']
            #set_status_ineligible(dn)
            logger.info('Created uniqname={}, continue to password'.format(form.cleaned_data['uniqname']))
            return redirect('password')
        else:
            logger.warning('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    # if a GET (or any other method)
    else:
        form = UniqnameForm()
        entry = mcomm_reg_umid_search(umid)
        dn = entry.entry_dn
        request.session['dn'] = dn    # We need dn to set password

        # If the user is not eligible, tell them nicely
        if not getuniq_eligible(entry):
            messages.error(request, settings.INELIGIBLE_ALERT_MSG)
            return redirect('terms')

        # If user has a uniqname, proceed as reactivate
        if 'umichRegUid' in entry:
            request.session['reactivate'] = True
            request.session['umid'] = umid
            request.session['uid'] = entry['umichRegUid'][0]
            logger.info('User has umichRegUid={}, proceed as reactivate'.format(entry['umichRegUid'][0]))
            return redirect('reactivate')

        # Kinda ugly, but we don't have name data if the admin app calls the web service
        if 'first_name' in data:
            first_name = data['first_name']
        else:
            first_name = entry['umichRegDisplayGivenName'][0]
        if 'last_name' in data:
            last_name = data['last_name']
        else:
            last_name = entry['umichRegDisplaySurname'][0]

        # Get uniqname suggestions based on the name data we have
        try:
            uniqname_suggestions = get_suggestions(dn, (first_name, last_name))
        except:
            messages.error(request, 'There was an issue generating suggestions, please try again.')
            uniqname_suggestions = ''

    context = {
        'form': form,
        'first_name': first_name,
        'last_name': last_name,
        'suggestions': uniqname_suggestions,
    }

    return render(request, 'create.html', context=context)


def test_create(request):

    if request.method == 'POST':
        form = UniqnameForm(request.POST)
        if form.is_valid():
            logger.debug('form={}'.format(form.cleaned_data))
            logger.debug('would have created uniqname {}'.format(form.cleaned_data['uniqname']))
            return redirect('password')
        else:
            logger.debug('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    else:
        dn = 'umichDirectoryID=161-0400-20150128095902514-557,ou=Identities,o=Registry'
        first_name = 'John'
        last_name = 'Doe'
        name_parts = (first_name, last_name)

        try:
            uniqname_suggestions = get_suggestions(dn, name_parts)
        except:
            logger.error('something failed')
            #messages.error(request, 'There was an issue generating suggestions, please try again.')
            uniqname_suggestions = ''

        uid = 'batman'
        umid = '12345678'
        source = 'anonymous'
        #create = uniqname_create(dn, uid, umid, source)

        form = UniqnameForm()

    context = {
        'form': form,
        'first_name': first_name,
        'last_name': last_name,
        'suggestions': uniqname_suggestions,
    }
    return render(request, 'create.html', context=context)


def reactivate(request):
    logger.info(request)
    logger.debug(request.session.items())

    reactivate = request.session.get('reactivate', False)
    dn = request.session.get('dn', False)
    umid = request.session.get('umid', False)
    uid = request.session.get('uid', False)

    # Make sure the user should be here
    if not (reactivate and dn and umid and uid):
        logger.debug('User does not need to be reactivated, redirecting to terms')
        return redirect('terms')

    # If this is a POST, verify the form and send them on to the success page if valid
    if request.method == 'POST':
        form = AcceptForm(request.POST)
        if form.is_valid():
            # do the reactivate
            reactivate_uniqname(dn, umid)
            #set_status_ineligible(dn)
            del request.session['reactivate']
            logger.info('Reactivated uid={}, continue to password'.format(uid))
            return redirect('password')
        else:
            logger.warning('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    else:
        form = AcceptForm()

    context = {
        'form': form,
        'uid': uid,
    }

    return render(request, 'reactivate.html', context=context)


def password(request):
    logger.info(request)
    logger.debug(request.session.items())

    uid = request.session.get('uid', False)

    # Make sure the user got here from a create or reactivate
    if not uid:
        logger.debug('User does not have a uid, redirecting to terms')
        return redirect('terms')

    # If this is a POST, verify the form and send them on to the success page if valid
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            if validate_passwords(uid, form.cleaned_data['password'], form.cleaned_data['confirm_password']):
                reset_password(uid, form.cleaned_data['password'])
                del request.session['uid']
                logger.info('Password changed, sending to success page')
                return redirect('success')
            else:
                form.add_error(None, "Passwords do not meet requirements")
        else:
            logger.warning('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    # GET or any other request generate a blank form
    else:
        form = PasswordForm()

    context = {
        'uid': uid,
        'form': form,
    }
    return render(request, 'password.html', context=context) 


def test_password(request):
    uid = 'tmp'

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            logger.debug('call validate_passwords')
            if validate_passwords(uid, form.cleaned_data['password'], form.cleaned_data['confirm_password']):
                logger.debug('TEST - reset password')
                return redirect('success')
            else:
                logger.debug('Passwords do not meet requirements')
                form.add_error(None, "Passwords do not meet requirements")
        else:
            logger.warning('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    else:
        form = PasswordForm()

    context = {
        'uid': uid,
        'form': form,
    }

    return render(request, 'password.html', context=context)

def success(request):
    logger.info(request)
    logger.debug(request.session.items())
    return render(request, 'success.html')


