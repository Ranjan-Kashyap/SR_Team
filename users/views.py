# users/views.py
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import CustomUser

from .forms import CustomUserCreationForm

def SignUp(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        form = CustomUserCreationForm(request.POST)
        email = request.POST['email']
        domain = email.split('@')[1]
        if domain != "sprintrise.com":
            return render(request, 'signup.html', {'error': 'Emails must be of SprintRise.com domain!'})
        else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = CustomUser.objects.get(email=request.POST['email'])
                    return render(request, 'signup.html', {'error': 'Account with this email already exists'})
                except CustomUser.DoesNotExist:
                    user = CustomUser.objects.create_user(email=request.POST['email'], full_name=request.POST['full_name'], date_of_birth=request.POST['date_of_birth'], password=request.POST['password1'])
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your SprintRise Team account.'
                    message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token':account_activation_token.make_token(user),
                    })
                    to_email = request.POST['email']
                    email = EmailMessage(
                    mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return HttpResponse('Please confirm your email address to complete the registration')
            else:
                    return render(request, 'signup.html', {'error': 'Passwords must match!'})
    else:
         # User wants to enter info
         return render (request, 'signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render (request, 'login.html', {'error': 'Email or Password is Incorrect'})
    else:
        return render (request, 'login.html')
