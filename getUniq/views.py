from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib import messages

from .forms import TermsForm, VerifyForm, TokenForm, UniqnameForm, PasswordForm
from .validate import validate_form_data 
from .token import generate_confirmation_token, confirm_token
from .uniqname_services import get_suggestions, uniqname_create

import logging

logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("Hello, world")


def terms(request):
    print(request)

    if request.method == 'POST':
        form = TermsForm(request.POST)
        if form.is_valid():
            print('form is valid')
            request.session['agreed_to_terms'] = True
            return redirect('verify')
        else:
            print('form invalid')
    else:
        form = TermsForm()

    return render(request, 'terms.html', {'form': form})


def verify(request):
    print(request)

    print(request.session)
    print(request.session.values())

    print('get={}'.format(request.session.get('agreed_to_terms', 'gear')))
    if request.session.get('agreed_to_terms', False):    # False is the default
        print('you agreed to our terms')
    else:
        print('you have not agreed to the terms yet')
        return redirect('terms')

    #return HttpResponse('Thanks')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = VerifyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            #logger.debug('form={}'.format(form.cleaned_data))
            print('form={}'.format(form.cleaned_data))
            entry = validate_form_data(form)
            if entry:
                #logger.debug('entry={}'.format(entry))
                print('entry={}'.format(entry))

                # mail testing
                token = generate_confirmation_token('psteffes@umich.edu')
                print('token={}'.format(token))

                secure_url = request.build_absolute_uri(reverse('create', args=[token]))
                #secure_url = reverse('create', args=[token])
                print('secure_url={}'.format(secure_url))

                plaintext = get_template('email.txt')
                html = get_template('email.html')
                d = {'secure_url': secure_url}
                subject = 'Please confirm your email'
                text_content = plaintext.render(d)
                html_content = html.render(d)

                send_mail(
                    subject,
                    text_content,
                    '4help@umich.edu',
                    ['psteffes@umich.edu'],
                    html_message=html_content,
                    fail_silently=False,
                )

                request.session['email'] = form.cleaned_data['email']
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


def confirm(request):
    print(request)

    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            print('form={}'.format(form.cleaned_data))
            if confirm_token(form.cleaned_data['token']):
                print('must be them')
                return redirect('confirmed')
            else:
                print('imposter')
                form.add_error(None, 'Unable to validate token')
        else:
            print('form.errors={}'.format(form.errors.as_json(escape_html=False)))
    else:
        form = TokenForm()

    return render(request, 'confirm.html', {'form': form})


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
        email = confirm_token(token)
        print('email={}'.format(email))
    except:
        print('imposter alert!')
        messages.error(request, 'The confirmation link is invalid or has expired, please try again.')
        return redirect('terms')

    if request.method == 'POST':
        form = UniqnameForm(request.POST)
        if form.is_valid():
            print('form={}'.format(form.cleaned_data))
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
            messages.error(request, 'There was an issue generating suggestions, please try again.')
            #uniqname_suggestions = ''
            uniqname_suggestions = ('name1', 'name2', 'name3')

        print('do not create yet')
        uid = 'batman'
        umid = '12345678'
        source = 'anonymous'
        #create = uniqname_create(dn, uid, umid, source)

        print('set up the stuff')
        form = UniqnameForm()
        context = {
            'form': form,
            'first_name': first_name,
            'last_name': last_name,
            'suggestions': uniqname_suggestions,
        }

    print('rendering create.html')
    return render(request, 'create.html', context=context)


def create2(request):

    if request.method == 'POST':
        form = UniqnameForm(request.POST)
        if form.is_valid():
            print('form={}'.format(form.cleaned_data))
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
            messages.error(request, 'There was an issue generating suggestions, please try again.')
            #uniqname_suggestions = ''
            uniqname_suggestions = ('name1', 'name2', 'name3')

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


def password(request):
    print(request)
    form = PasswordForm()
    return render(request, 'password.html', {'form': form}) 
