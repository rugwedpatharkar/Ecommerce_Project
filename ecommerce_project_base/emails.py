import imp
from django.conf import settings
from django.core.mail import send_mail



def send_account_activation_email(email, email_token):
    subject = 'Activate Your Account on Gadget Galaxy - Your Ultimate Tech Gadgets Destination'
    message = f'''
Thank you for joining Gadget Galaxy – Your Ultimate Tech Gadgets Destination!

We are excited to welcome you to our tech-savvy community.

To activate your account and unlock the latest in tech innovations, click on the following link:

http://127.0.0.1:8000/accounts/activate/{email_token}

Please be aware that this link is valid for a limited time. If you did not request this activation, you can safely disregard this email.

Get ready to embark on a journey of discovery at Gadget Galaxy! Explore the latest gadgets and elevate your tech experience.

Best regards,
The Gadget Galaxy Team
'''


    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])