from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage
import re


def signin(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        if username == "" or username is None:
            messages.error(request,'Username must not be empty')
            return redirect('signin')

        if password == "" or password is None:
            messages.error(request,'Password must not be empty')
            return redirect('signin')

        user = User.objects.get(username=username)
        if user and authenticate(request, username=username, password=password):
            login(request, user)
        else:
            messages.error(request,'Invalid username or password')
            return redirect('signin')

        return redirect('discover')

    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname'].strip()
        lastname = request.POST['lastname'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        retype_password = request.POST['retypepassword'].strip()
        
        if firstname == "" or firstname is None:
            messages.error(request,'First Name is Empty or It is not Valid')
            return redirect('signup')
        
        if lastname == "" or lastname is None:
            messages.error(request,'Last Name is Empty or It is not Valid')
            return redirect('signup')

        if username == "" or username is None:
            messages.error(request,'Username is Empty or It is not Valid')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request,'A user already exists with the given username')
            return redirect('signup')

        EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if email and not re.match(EMAIL_REGEX, email):
            messages.error(request,'Email is Empty or It is not Valid')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request,'A user already exists with the given email')
            return redirect('signup')

        PASSWORD_REGEX = r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$"
        if password == "" or not re.match(PASSWORD_REGEX, password):
            messages.error(request,'Password is Empty or It is not Valid. It must have a length of [6,12] with atleast one uppercase letter, lowercase letter, a digit and a special character.')
            return redirect('signup')

        if retype_password and retype_password != password:
            messages.error(request,'Retype Password does not match with the password')
            return redirect('signup')

        user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, 
                                        email=email, password=password)
        user.is_active = False
        user.save()
        
        current_site = get_current_site(request)
        message = render_to_string('acc_active_email.html', {
            'user':user, 'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        mail_subject = 'Activate your account.'
        to_email = email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        
        return render(request, 'message.html', {'message': 'Please confirm your email address to complete the registration.'}) 
    
    return render(request, 'signin.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('discover')
    else:
        return render(request, 'message.html', {'message': 'Activation link is invalid!'})

def logout(request):
    logout(request)
    return redirect('signin')