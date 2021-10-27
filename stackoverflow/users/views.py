from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .tokens import account_activation_token
from .models import User
from questions.models import Question, Answer
from django.db.models import Count
import json
import datetime


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

        return redirect('feed')

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
        # Save User if Verification Mail Successfully Sent
        user.save()
        
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
        return render(request, "profile.html", { 'user': request.user })
    else:
        messages.error(request,'Activation link is invalid!')
        return render(request, 'signin.html')

@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def profile(request):
    if request.method == 'POST':
        firstname = request.POST['firstname'].strip()
        middlename = request.POST['middlename'].strip()
        lastname = request.POST['lastname'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        birthdate = request.POST['birthdate'].strip()
        age = int(request.POST['age'].strip().split()[0])
        bio = request.POST['bio'].strip()
        profession = request.POST['profession'].strip()
        organization = request.POST['organization'].strip()
        gender = request.POST['gender'].strip()
        mobilenumber = request.POST['mobilenumber'].strip()
        pincode = request.POST['pincode'].strip()
        city = request.POST['city'].strip()
        country = request.POST['country'].strip()
        skills = json.dumps(request.POST['skills'])
        # print(firstname, middlename, lastname, username, email, birthdate, age, bio, profession, organization, gender, mobilenumber, pincode, city, country, skills)
        
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
                if birthdate:
                    date_format = '%d/%m/%Y'
                    user.birth_date = datetime.datetime.strptime(birthdate, date_format).date()
                else:
                    user.birth_date = None
                if age:
                    user.age = age
                else:
                    user.age = None
                user.bio = bio
                user.profession = profession
                user.organization = organization
                user.gender = gender
                user.mobile_number = mobilenumber
                user.pincode = pincode
                user.city = city
                user.country = country
                user.skills = skills
                # print(user)

                if request.FILES.get('profilepicture', False):
                    profile_picture = request.FILES['profilepicture']
                    # print(profile_picture)
                    if user.profile_picture != 'profile_pics/default.svg':
                        user.profile_picture.storage.delete(user.profile_picture.name)
                    # fss = FileSystemStorage(location=settings.PROFILE_PICTURE_STORAGE)
                    # print(profile_picture.name)
                    # filename = fss.save(profile_picture.name, profile_picture)
                    # user.profile_picture = profile_picture
                    # user.profile_picture.name = filename
                    user.profile_picture = profile_picture

                user.save()

                messages.success(request,'Profile Updated Successfully')
                return redirect('profile')
    
        messages.error(request,'Failed to update Profile... Try Again')

    current_user = request.user
    users = Answer.objects.filter(is_accepted=True).values('user').annotate(ac_count=Count('user')).order_by('-ac_count')
    num_of_users = len(users)
    current_user_index = next((index for index in range(num_of_users) if users[index]['user'] == current_user.id), None)

    # print(users)
    # print(num_of_users, current_user_index)

    badge = None
    if current_user_index is not None:
        rank = round(current_user_index / num_of_users * 100)
        badge = 'Gold' if rank <= 10 else 'Silver' if rank <= 25 else 'Bronze' if rank <= 50 else None

    # print(rank, badge)

    return render(request, 'profile.html', { 'user': current_user, 'badge': badge })

