from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .tokens import account_activation_token
from .models import User
import json


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

        return redirect('home')

    return render(request, 'signin.html')


@csrf_exempt
def check_username(request, username):
    if request.method == 'POST':
        user_exists = False
        if username and username != "":
            user_exists = User.objects.filter(username=username).exists()
        return JsonResponse({ 'exists': user_exists })

@csrf_exempt
def check_email(request, email):
    if request.method == 'POST':
        email_exists = False
        if email and email != "":
            email_exists = User.objects.filter(email=email).exists()
        return JsonResponse({ 'exists': email_exists })

def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname'].strip()
        lastname = request.POST['lastname'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

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
        return redirect('home')
    else:
        return render(request, 'message.html', {'message': 'Activation link is invalid!'})

def signout(request):
    logout(request)
    return redirect('signin')

def profile(request):
    if request.method == 'POST':
        firstname = request.POST['firstname'].strip()
        middlename = request.POST['firstname'].strip()
        lastname = request.POST['lastname'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        birthdate = request.POST['birthdate']
        age = request.POST['age']
        bio = request.POST['bio'].strip()
        profession = request.POST['profession'].strip()
        organization = request.POST['organization'].strip()
        gender = request.POST['gender'].strip()
        phone = request.POST['phone'].strip()
        country = request.POST['country'].strip()
        skills = json.dumps(request.POST['skills'])
        
        current_user = request.user

        if current_user.id is not None:
            user = User.objects.get(pk=current_user.id)
            
            if user is not None:
                user.first_name = firstname
                user.middle_name = middlename
                user.last_name = lastname
                user.username = username
                user.email = email
                user.birth_date = birthdate
                user.age = age
                user.bio = bio
                user.profession = profession
                user.organization = organization
                user.gender = gender
                user.phone = phone
                user.country = country
                user.skills = skills

                if user.profile_picture != 'default.png':
                    user.profile_picture.storage.delete(user.profile_picture.name)

                profile_picture = request.FILES['profile-picture']
                fss = FileSystemStorage(location=settings.PROFILE_PICTURE_STORAGE)
                filename = fss.save(profile_picture.name, profile_picture)
                user.profile_picture = profile_picture
                user.profile_picture.name = filename

                user.save()
        
        return redirect('profile')
    
    return render(request, 'profile.html', { 'user': request.user })

