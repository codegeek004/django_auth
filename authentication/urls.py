from django.urls import path
from .views import *
urlpatterns = [
            path('', index, name='index'),
            path('register/', register_view, name='register'),
            path('user_login/', user_login, name='user_login'),
            path('logout/', logout_view, name='logout_view'),
            path('login/oid/', oidc_login, name='oidc_login'),
            path('logout/oidc/', oidc_logout, name='oidc_logout'),
            path("callback", callback, name="callback"),
        ]
