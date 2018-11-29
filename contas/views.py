from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages
from contas.models import Token
from django.core.urlresolvers import reverse

def envia_email_login(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    corpo_do_email = f'Use este link para logar:\n\n{url}'
    
    send_mail('Seu link para login no BikeUnit',
              corpo_do_email,
              'noreply@bikeunit.com', 
              [email]
    )

    messages.success(
        request,
        'Verifique seu email, te enviamos um link para que você possa acessar.'
    )
    return redirect('/')

def login(request):
    return redirect('/')
