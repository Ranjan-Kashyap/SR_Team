# users/views.py
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import CustomUser
from datetime import timedelta, date

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
                    user = CustomUser.objects.create_user(
                        email=request.POST['email'], full_name=request.POST['full_name'], date_of_birth=request.POST['date_of_birth'], password=request.POST['password1'])
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your SprintRise Team account.'
                    message = render_to_string('acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = request.POST['email']
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return render(request, 'email_confirmation.html')
            else:
                return render(request, 'signup.html', {'error': 'Passwords must match!'})
    else:
        # User wants to enter info
        return render(request, 'signup.html')


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
        return redirect('home')
    else:
        return render(request, 'activation_link_invalid.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Email or Password is Incorrect'})
    else:
        return render(request, 'login.html')


def password_reset(request):
    return render(request, 'registration/password_reset_form.html')


def get_upcoming_birthdays(request):
    users_list = CustomUser.objects.values()
    person_list = users_list.distinct()
    days = 5
    today = date.today()
    birthday_person = []
    birthday_person.extend(list(person_list.filter(
        date_of_birth__month=today.month, date_of_birth__day=today.day)))
    doblist = []
    doblist.extend(list(person_list.filter(
        date_of_birth__month=today.month, date_of_birth__day=today.day)))
    next_day = today + timedelta(days=1)
    for day in range(0, days):
        doblist.extend(list(person_list.filter(
            date_of_birth__month=next_day.month, date_of_birth__day=next_day.day)))
        next_day = next_day + timedelta(days=1)

    for item in doblist:  # Modify key strings the list of dictionaries
        item["Name"] = item.pop("full_name")
        item["Date of Birth"] = item.pop("date_of_birth")
    # list to mention only required keys
    wanted_keys = ['Name', 'Date of Birth']
    if len(birthday_person) == 0:
        return render(request, 'upcoming_birthdays.html', {'doblist': doblist, 'wanted_keys': wanted_keys})
    else:
        names = []
        for name in birthday_person:
            names.append(name.get('full_name'))
        return render(request, 'upcoming_birthdays.html', {'birthday_person': names, 'doblist': doblist, 'wanted_keys': wanted_keys})


# return render(request, 'upcoming_birthdays.html', {'upcoming_birthdays':
# doblist})
