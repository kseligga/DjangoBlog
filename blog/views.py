from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from blog.models import Post, Comment, Response, Thread, UserProfile
from .forms import CommentForm, UserRegisterForm, ResponseForm, ThreadForm, CommentLoggedForm, PasswordResetConfirmForm


def index(request):
    return render(request, 'blog/homepage.html')


def post(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-pub_date')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentLoggedForm(request.POST)
            if form.is_valid():
                c = Comment(post=post,
                            author=request.user.username,
                            content=form.cleaned_data["comment"],
                            pub_date=timezone.now())
                c.save()
                return HttpResponseRedirect(f'/blog/posts/{post.id}')
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                c = Comment(post=post,
                            author=form.cleaned_data["my_name"],
                            content=form.cleaned_data["comment"],
                            pub_date=timezone.now())
                c.save()
                return HttpResponseRedirect(f'/blog/posts/{post.id}')
    else:
        if request.user.is_authenticated:
            form = CommentLoggedForm()
        else:
            form = CommentForm()

    context = {'post': post,
               'comments': comments,
               'form': form}

    return render(request, 'blog/post.html', context=context)


def blog(request):
    posts = Post.objects.order_by('-pub_date')
    contextt = {'list_of_posts': posts}
    return render(request, 'blog/blog.html', context=contextt)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('/homepage')
        else:
            return render(request, 'blog/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'blog/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'blog/loggedout.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            UserProfile.objects.create(
                user=user,
                reason=form.cleaned_data.get('reason'),
                birthDate=form.cleaned_data.get('birthDate'),
                sex=form.cleaned_data.get('sex')
            )

            # Email verification
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('blog/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'noreply@epilepsyforum.com', [user.email])
            return redirect('account_activation_sent')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'blog/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'blog/activation_invalid.html')


def forum_view(request):
    threads = Thread.objects.order_by('-pub_date')
    form = ThreadForm()
    context = {'list_of_threads': threads, 'form': form}

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            t = Thread(title=form.cleaned_data["title"],
                       author=request.user.username,
                       content=form.cleaned_data["content"],
                       pub_date=timezone.now())
            t.save()
            return HttpResponseRedirect(f'/forum/')
        else:
            # Add this else clause to handle the case where the form is not valid
            return render(request, 'blog/forum.html', context=context)
    else:
        return render(request, 'blog/forum.html', context=context)


def thread(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    responses = Response.objects.filter(thread=thread).order_by('-pub_date')

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            r = Response(thread=thread,
                         author=request.user.username,
                         content=form.cleaned_data["response"],
                         pub_date=timezone.now())
            r.save()
            return HttpResponseRedirect(f'/forum/threads/{thread.id}')
    else:
        form = ResponseForm()

    context = {'thread': thread,
               'responses': responses,
               'form': form}

    return render(request, 'blog/thread.html', context=context)


def epilepsytest_view(request):
    return render(request, 'blog/epilepsy-test.html')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    # user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'user': user,
        'username': user.username,
        'email': user.email,
        # add any other user fields you want to display
    }

    return render(request, 'blog/profile.html', context=context)


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # Here you can add the logic to send the email
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                mail_subject = 'Reset your password.'
                message = render_to_string('blog/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                send_mail(mail_subject, message, 'noreply@epilepsyforum.com', [user.email])
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'blog/password_reset.html', {'form': form})


def password_reset_done(request):
    return render(request, 'blog/password_reset_done.html')


def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetConfirmForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = PasswordResetConfirmForm(user)
    else:
        form = None
    return render(request, 'blog/password_reset_confirm.html', {'form': form})
