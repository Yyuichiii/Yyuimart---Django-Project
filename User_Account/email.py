from django.conf import settings
from django.core.mail import send_mail

email_from = settings.EMAIL_HOST_USER


# Send Email for refistration
def registration_email(name,email):
    subject = 'Welcome to Yyuicart !!!'
    message = 'Hi '+name+' thank you for creating the account in Yyuicart.\n\nHope you have a good day ahead !!!'
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )

# Email for Password Change
def password_email(name,email):
    subject = 'Password Changed !!!'
    message = 'Hi '+name+' ,your password as been changed successfully.\n\nHope you have a good day ahead !!!\n\nRegards Team Yyuicart'
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )


# Email for Recieved Order
def order_recieved(email):
    subject = 'Order Recieved !!!'
    message = 'Your order has been successfully recieved.\n\nHope you have a good day ahead !!!\n\nRegards Team Yyuicart'
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )



# Email for OTP CONFIRMATION
def email_otp(generated_otp,email):
    subject = 'OTP !!!'
    message = 'The OTP for the registration of your Account is:.\n\n'+generated_otp+ '\n\nRegards Team Yyuicart'
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )