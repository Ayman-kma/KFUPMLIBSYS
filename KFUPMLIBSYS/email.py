# import django.core.mail as send_mail
from django.core.mail import send_mail


# from django.conf import settings
send_mail('sss','hhh','ayman.sensie@gmail.com',['kfupmlibsys@yahoo.com'])

# send_mai
# def send_email(request):
#     msg = EmailMessage('Request Callback',
#                        'Here is the message.', to=['ayman.sensie@gmail.com'])
#     msg.send()
#     return HttpResponseRedirect('/')
    