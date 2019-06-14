from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Post
from .tokens import account_activation_token, password_reset_token
from .forms import PostForm, NewUserForm

# Create your views here.

def homepage(request):
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.post_owner=request.user
            post.save()
            return redirect('main:homepage')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = PostForm
    return render(request=request, template_name='main/index.html', context={'posts': Post.objects.all, 'form': form})


def detail(request, post_id):
    return render(request=request, template_name='main/detail.html', context={'post': Post.objects.get(pk=post_id)})

def view_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect('main:homepage')
    return render(request=request, template_name='main/user.html', context={'user': User.objects.get(pk=user_id)})


def edit(request, post_id):
    if Post.objects.get(pk=post_id).post_owner == request.user:
        print('reached here')
        post = Post.objects.get(pk=post_id)
        form = PostForm(instance=post)
        if request.method == 'POST':
            f = PostForm(request.POST, instance=post)
            f.save()
            return redirect('main:myposts')
        return render(request=request, template_name='main/index.html', context={'form': form})
    return redirect('main:homepage')


def delete(request, post_id):
    if Post.objects.get(pk=post_id).post_owner == request.user:
        Post.objects.get(pk=post_id).delete()
        return redirect('main:myposts')
    return redirect('main:homepage')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in as {username}")
                return redirect('main:homepage')

        else:
            messages.error(request, f"Invalid username or password")
    if request.user.is_authenticated:
        return redirect('main:homepage')
    form = AuthenticationForm
    return render(request=request, template_name='main/login.html', context={'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, f"Logged out successfully")
    return redirect('main:homepage')


def register_request(request):
    if request.method=='POST':
        form=NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()

            current_site = get_current_site(request)

            username = form.cleaned_data.get("username")
            email_to_address = form.cleaned_data.get("email")

            email_subject = "Activate your account on Django Social Network"
            email_message = render_to_string('main/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_from_address = 'django-admin@django-social-network.com'

            try:
                send_mail(email_subject, email_message, email_from_address, [email_to_address], html_message=email_message)
            except Exception as e:
                print(e)


            messages.success(request, f"New account created for {username}")
            # login(request, user)
            messages.info(request, f"Confirm the email sent to {email_to_address}")
            return redirect('main:homepage')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    if request.user.is_authenticated:
        return redirect('main:homepage')

    form = NewUserForm
    return render(request=request, template_name='main/register.html', context={'form': form})


def profile_request(request):
    if not request.user.is_authenticated:
        return redirect('main:homepage')
    user = request.user
    return render(request=request, template_name='main/profile.html', context={"user": user})


def user_posts(request):
    if not request.user.is_authenticated:
        return redirect('main:homepage')
    return render(request=request, template_name='main/myposts.html', context={'posts': Post.objects.filter(post_owner=request.user)})


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
        messages.info(request, 'Account activated')
        return redirect('main:homepage')
    else:
        return HttpResponse('Activation link is invalid.')


def forgot_password(request):
    if request.method=='POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email_to_address = form.cleaned_data.get('email')

            if (email_to_address, ) not in User.objects.values_list('email'):
                print('here')
                return redirect('main:homepage')
                messages.error(request, f"The email you entered was incorrect")

            user = User.objects.get(email=email_to_address)
            current_site = get_current_site(request)
            email_subject = "Reset password for your account on Django Social Network"
            email_message = render_to_string('main/password_reset.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': password_reset_token.make_token(user),
            })
            email_from_address = 'django-admin@django-social-network.com'

            try:
                send_mail(email_subject, email_message, email_from_address, [email_to_address], html_message=email_message)
            except Exception as e:
                print(e.message)

            messages.info(request, f"A password reset link has been sent to {email_to_address}")
            return redirect('main:homepage')

    form = PasswordResetForm
    return render(request=request, template_name='main/password_reset_form.html', context={'form': form})

def reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method=='POST':
        if user is not None and password_reset_token.check_token(user, token):
            form = SetPasswordForm(user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f"Password reset successfully, please login with new password")
                return redirect('main:login')
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
                return render(request, template_name="main/reset.html", context={'form': form})
        else:
            return HttpResponse('Reset link is invalid.')


    else:
        if user is not None and password_reset_token.check_token(user, token):
            form = SetPasswordForm(user)
            return render(request, template_name="main/reset.html", context={'form': form})
        else:
            return HttpResponse('Reset link is invalid')




