from django.urls import path
from .views import *
urlpatterns = [
            path('', index, name='index_view'),
            path('register/', register_view, name='register'),
            path('user_login/', user_login, name='user_login'),
            path('logout/', logout_view, name='logout_view')
        ]
