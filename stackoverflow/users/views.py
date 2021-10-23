from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
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

        try:
            user = User.objects.get(username=username)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and authenticate(request, username=username, password=password):
            login(request, user)
        else:
            messages.error(request,'Invalid username or password')
            return redirect('signin')

        return render(request, 'discover.html', {"username": user.username})

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
        retypepassword = request.POST['retypepassword'].strip();

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signin')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signin')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signin')
        
        if password != retypepassword:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signin')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signin')

        user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, 
                                        email=email, password=password)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        email_subject = "Welcome to DevTalks!! Please Confirm your Email Address ..."
        ctx = dict({
            'username': user.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        message = get_template('welcome.html').render(ctx)
        email = EmailMultiAlternatives(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.content_subtype = 'html'
        email.fail_silently = True
        email.send()
        
        messages.success(request,'A confirmation link has been sent to your Email Id.')
        return redirect('signin')
    
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
        messages.success(request,'Account has been activated!!')
        return render(request, "profile.html",{"firstName": user.first_name, "lastName": user.last_name, "username": user.username, "email": user.email})
    else:
        messages.error(request,'Activation link is invalid!')
        return render(request, 'signin.html')

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
            try:
                user = User.objects.get(pk=current_user.id)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            
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

