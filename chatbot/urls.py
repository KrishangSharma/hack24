from django.urls import include, path
from . import views

urlpatterns=[
    path('', views.chatbot, name='chatbot'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    # path('sentiments', views.view_sentiments, name='view_sentiments' ),
    path('user_profile', views.user_profile, name='user_profile'),
    path('chat_history', views.chat_history, name='chat_history'),
    path('status_tracking', views.status_tracking, name='status_tracking'),
    path('change-password', views.change_password, name='change_password')
]