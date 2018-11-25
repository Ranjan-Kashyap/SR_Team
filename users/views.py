# users/views.py
from django.shortcuts import render, redirect
from django.contrib import auth
from .models import CustomUser

from .forms import CustomUserCreationForm

# class SignUp(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'

def SignUp(request):
    if request.method == 'POST':
        # User has info and wants an account now!
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
                    auth.login(request, user)
                    return redirect('home')
            else:
                return render(request, 'signup.html', {'error': 'Passwords must match!'})
    else:
         # User wants to enter info
         return render (request, 'signup.html')

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
