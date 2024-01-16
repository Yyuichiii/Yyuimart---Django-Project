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


# Email for Recieved Orders
def order_recieved(Queryset,email,tp):
    subject = 'Order Recieved !!!'
    intro="Thank You for shopping at Yyuimart.\n\nWe have recieved an order of:\n"
    dic=""
    i=0
    for a in Queryset:
        m=str(i+1)+") "+str(a.Brand) +" "+ str(a.PName)+"\nPrice: Rs. " + str(a.Price)+"/-\nQuantity:" + str(a.Quantity)+"\n\n"
        i=i+1
        dic=dic+m
        
    message=intro+dic+"The total Price is Rs. "+str(tp)+"/- with shipping charges included."+"\n\nRegards Team Yyuimart "
    
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )


# Email for OTP CONFIRMATION
def email_otp(generated_otp,email):
    subject = 'OTP !!!'
    message = 'The OTP for the registration of your Account is:.\n\n'+generated_otp+ '\n\nRegards Team Yyuicart'
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )