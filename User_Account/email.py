from django.conf import settings
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
email_from = settings.EMAIL_HOST_USER

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