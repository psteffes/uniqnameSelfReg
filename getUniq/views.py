from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib import messages

from .forms import AcceptForm, VerifyForm, TokenForm, UniqnameForm, PasswordForm
from .idproof import idproof_form_data 
from .token import generate_confirmation_token, confirm_token
from .uniqname_services import get_suggestions, create_uniqname, reactivate_uniqname
from .utils import getuniq_eligible
from .myldap import mcomm_reg_umid_search

import logging

logger = logging.getLogger(__name__)


def terms(request):
    try:
        print(request)

        if request.method == 'POST':
            form = AcceptForm(request.POST)
            if form.is_valid():
                print('form is valid')
                request.session['agreed_to_terms'] = True
                return redirect('verify')
            else:
                print('form invalid')
        else:
            form = AcceptForm()
    except Exception as e:
        print('terms error={}'.format(e))
        raise

    return render(request, 'terms.html', {'form': form})


def verify(request):
    print(request)
    print(request.session)
    print(request.session.values())

    if request.session.get('agreed_to_terms', False):    # False is the default
        print('you agreed to our terms')
    else:
        print('you have not agreed to the terms yet')
        return redirect('terms')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VerifyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            #logger.debug('form={}'.format(form.cleaned_data))
            print('form={}'.format(form.cleaned_data))
            entry = idproof_form_data(form.cleaned_data)
            if entry:
                #logger.debug('entry={}'.format(entry))
                print('entry={}'.format(entry))

                # If the person is not eligible, tell them nicely
                #if 'umichGetUniqEntitlingRoles' not in entry or entry['umichGetUniqStatus'] != 'STARTED':
                if not getuniq_eligible(entry):
                    messages.error(request, 'You are not eligible')
                    return redirect('terms')
                else:
                    print('entry.umichGetUniqEntitlingRoles={}'.format(entry['umichGetUniqEntitlingRoles']))

                # Generate the token and build the secure link
                #data = [entry['umichRegEntityID'], form.cleaned_data['first_name'], form.cleaned_data['last_name']]
                data = {
                    'umid': entry['umichRegEntityID'],
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                }
                token = generate_confirmation_token(data)
                secure_url = request.build_absolute_uri(reverse('create', args=[token]))
                print('secure_url={}'.format(secure_url))

                # mail testing
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

                request.session['email'] = email
                return redirect('confirm_email')
            else:
                form.add_error(None, 'Unable to validate identity')
        else:
            #logger.warn('form.errors={}'.format(form.errors.as_json(escape_html=False)))
            print('form.errors={}'.format(form.errors.as_json(escape_html=False)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = VerifyForm()

    return render(request, 'verify.html', {'form': form})


def confirm_email(request):
    print(request)
    email = request.session.get('email', False)
    if email:
        context = {'email': email}
        return render(request, 'confirm_email.html', context)
    else:
        return redirect('terms')


def create(request, token):
    print(request)
    print(token)

    try:
        data = confirm_token(token)
        print('data={}'.format(data))
        umid = data['umid']
        print('umid={}'.format(umid))
    except:
        print('imposter alert!')
        messages.error(request, 'The confirmation link is invalid or has expired, please verify your identity and try again.')
        return redirect('terms')

    dn = request.session.get('dn', False)

    if request.method == 'POST':
        form = UniqnameForm(request.POST)
        if form.is_valid() and dn:
            print('form={}'.format(form.cleaned_data))
            request.session['uid'] = form.cleaned_data['uniqname']
            create_uniqname(dn, form.cleaned_data['uniqname'], umid)
            return redirect('password')
        else:
            print('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    else:
        ###
        entry = mcomm_reg_umid_search(umid)
        dn = entry.entry_dn
        request.session['dn'] = dn

        # If the person is not eligible, tell them nicely
        if not getuniq_eligible(entry):
            messages.error(request, 'You are not eligible')
            return redirect('terms')

        if 'umichRegUid' in entry:
            print('this is a reactivate')
            request.session['reactivate'] = True
            request.session['umid'] = umid
            request.session['uid'] = entry['umichRegUid'][0]
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

        try:
            uniqname_suggestions = get_suggestions(dn, (first_name, last_name))
        except:
            messages.error(request, 'There was an issue generating suggestions, please try again.')
            uniqname_suggestions = ''

        form = UniqnameForm()

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
            print('form={}'.format(form.cleaned_data))
            print('would have created uniqname {}'.format(form.cleaned_data['uniqname']))
            return redirect('password')
        else:
            print('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    else:
        dn = 'umichDirectoryID=161-0400-20150128095902514-557,ou=Identities,o=Registry'
        first_name = 'John'
        last_name = 'Doe'
        name_parts = (first_name, last_name)

        try:
            uniqname_suggestions = get_suggestions(dn, name_parts)
        except:
            print('something failed')
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
    print(request)
    print(request.session)
    print(request.session.values())
    print('get={}'.format(request.session.get('agreed_to_terms', 'gear')))
    print('get={}'.format(request.session.get('umid', 'gear')))

    reactivate = request.session.get('reactivate', False)
    dn = request.session.get('dn', False)
    umid = request.session.get('umid', False)
    uid = request.session.get('uid', False)

    if reactivate and dn and umid:
        print('reactivate dn={} umid={}'.format(dn, umid))        
    else:
        print('we do not need to reactivate you')
        return redirect('terms')

    if request.method == 'POST':
        form = AcceptForm(request.POST)
        if form.is_valid():
            print('form is valid reactivate and send them to password')
            # do the reactivate
            reactivate_uniqname(dn, umid) 
            return redirect('password')
        else:
            print('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    else:
        form = AcceptForm()

    context = {
        'form': form,
        'uid': uid,
    }

    return render(request, 'reactivate.html', context=context)


def password(request):
    print(request)
    print(request.session)
    print(request.session.values())

    uid = request.session.get('uid', False)

    # Make sure the user got here from a create or reactivate
    if uid:
        print('session.uid={}'.format(uid))
    else:
        print('you do not have a uid you liar')
        return redirect('terms')

    # If this is a POST, verify the form and send them on to the success page if valid
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            print('set password')
            reset_password(uid, form.cleaned_data['password'])
            return redirect('success')
        else:
            print('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    # GET or any other request generate a blank form
    else:
        form = PasswordForm()

    context = {
        'uid': uid,
        'form': form,
    }
    return render(request, 'password.html', context=context) 


def test_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            print('TEST - reset password')
            return redirect('success')
        else:
            print('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    else:
        form = PasswordForm()

    return render(request, 'password.html', {'form': form})

def success(request):
    print(request)
    return render(request, 'success.html')


def otid(request):
    print(request)
    return render(request, 'otid.html')
