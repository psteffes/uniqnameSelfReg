from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

def send_confirm_email(to_address, first_name, last_name, secure_url):
    """Send the confirmation email to the passed address"""

    plaintext = get_template('email.txt')
    d = {
        'first_name': first_name,
        'last_name': last_name,
        'secure_url': secure_url,
    }
    subject = 'Complete Your U-M Uniqname & Account Setup'
    text_content = plaintext.render(d)
    email = EmailMessage(
        'Complete Your U-M Uniqname & Account Setup',
        text_content,
        settings.EMAIL_FROM_ADDRESS,
        [to_address],
        reply_to=[settings.EMAIL_REPLY_TO],
    )
    email.send(fail_silently=False)

    return 
