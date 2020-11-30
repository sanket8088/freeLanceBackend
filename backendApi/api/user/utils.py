from backendApi import settings
from django.core.mail import send_mail

#html email sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def sendMail(instance,message):
    subject = "Password Reset"
    msg = message
    to = instance
    # res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    html_content = render_to_string("email.html", {"message": settings.UI_URL+"/forgotpassword/"+message})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [to]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    # print("True", res)

def emailConfirmation(instance,message):
    subject = "New User Registration"
    msg = message
    to = instance
    # res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    html_content = render_to_string("email_confirmation.html", {"message": settings.HOSTED_URL+"/api/user/confirm_email/"+message})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        "sanket.nihal2@gmail.com",
        [to]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    # print("True", res)

