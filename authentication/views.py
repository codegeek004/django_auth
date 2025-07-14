from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User  
from .models import CustomUser
import json
from authlib.integrations.django_client import OAuth    
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

def index(request):
    context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        }
    return render(request, 'index.html', context)

def register_view(request):
    print('inside register view')
    if request.method == 'POST':
        print('in post method')
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        print(f'username, {username}, password, {password}, contact, {contact}')

        if CustomUser.objects.filter(username=username).exists():
            print('user exists')
            messages.error(request, 'username already taken')
        else:
            print('inside else')
            user = CustomUser.objects.create(
                    username=username,
                    contact=contact
                )
            print('user',user)
            user.set_password(password)
            user.save()
            messages.info(request, 'user created successfully')
            print('created successflly')
            return redirect('user_login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username not found. Please register first')
        user = authenticate(username=username, password=password)
        print(user, 'checking activity')
        if user is None:
            messages.error(request, 'Invalid username or password')
        else:
            login(request, user)
            return render(request, 'index.html')
    return render(request, 'basic_login.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return render(request, 'index.html')



oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def oidc_login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

def oidc_logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )