from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
email_from = settings.EMAIL_HOST_USER
# celery -A Yyuimart  worker -l INFO


# Email for OTP CONFIRMATION
def email_otp(generated_otp,email,name):
    subject = 'OTP Verification on '+settings.SITE_NAME
    from_email = settings.EMAIL_HOST_USER
    to = [email]
    data={
        'otp':generated_otp,
        'Name':name,
        'Company':settings.SITE_NAME
    }
     # Load the HTML template
    html_content = render_to_string('User_Account/otp_email.html', {'data': data})
    # Create the email body with both HTML and plain text versions
    text_content = strip_tags(html_content)   
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()



# Email for successful Registration
@shared_task
def email_success_register(email,name):
    subject = 'OTP Verification on '+settings.SITE_NAME
    from_email = settings.EMAIL_HOST_USER
    to = [email]
    data={
        'Name':name,
        'Company':settings.SITE_NAME
    }
     # Load the HTML template
    html_content = render_to_string('User_Account/register_success_email.html', {'data': data})
    # Create the email body with both HTML and plain text versions
    text_content = strip_tags(html_content)   
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()


# Email for Password Change
@shared_task    
def password_email(name,email):
    subject = 'Password Changed !!!'
    from_email = settings.EMAIL_HOST_USER
    to = [email]
    data={
        'Name':name,
        'Company':settings.SITE_NAME
    }
    # Load the HTML template
    html_content = render_to_string('User_Account/password_change_email.html', {'data': data})
    # Create the email body with both HTML and plain text versions
    text_content = strip_tags(html_content)   
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()
    

# Email for Recieved Order

# @shared_task
def order_recieved(order,email,total_price):
    subject = 'Order Confirmed !!!'
    from_email = settings.EMAIL_HOST_USER
    to = [email]
    data={
        'Company':settings.SITE_NAME,
        'order_items_list':order,
        'total_amount':total_price
    }
    # Load the HTML template
    html_content = render_to_string('User_Account/order_email.html', {'data': data})
    # Create the email body with both HTML and plain text versions
    text_content = strip_tags(html_content)   
    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()