from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from .token import account_activation_token
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail 
from django.contrib.auth.decorators import login_required
# from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import IntegrityError
from .models import Profile, ProfilePic

from .forms import RegisterForm, LoginForm, ProfileForm, AvatarForm

@login_required
def index(request):
    context = {}

    return render(request, 'users/dashboard/index.html', context)

def sent(request):
    return render(request, 'users/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'users/account_activation_invalid.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Site Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = RegisterForm()
    context = {
            'form': form,
        }
    return render(request, 'users/register.html', context)


def auth_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('dashboard')
    else:
        form = LoginForm()
        messages.error(request,'username or password not correct')
        context = {
            'form':form
        }
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')   

@login_required
def user_settings(request):
    profile = get_object_or_404(Profile, user=request.user)
    profilepic = get_object_or_404(ProfilePic, user=request.user)
    form = ProfileForm(data=request.POST, instance=profile)
    avatarform = AvatarForm(request.POST or None, request.FILES or None, instance=profilepic)

    if form.is_valid():
        try:
            profile = form.save(commit=False)
            profile.user = request.user
            User.objects.values('username').filter(username=request.user).update(username=profile.username)
            profile.save()
        except IntegrityError:
            messages.warning(request, 'This username has already been taken!')
        return redirect('user_settings')
    else:
        form = ProfileForm()

    if avatarform.is_valid():
            profilepic = avatarform.save(commit=False)
            profilepic.user = request.user
            profilepic.save()
    else:
        avatarform = AvatarForm()

    context = {
        'form':form,
        'profile':profile,
        'avatarform':avatarform,
        'profilepic':profilepic,   
    }
    return render(request, 'users/dashboard/settings.html', context )