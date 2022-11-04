from django.urls import path, include
from . import views

app_name= 'chat'

urlpatterns = [
    path('', views.ChatView.as_view(), name='main'),
    path("chat/<str:chat_box_name>/", views.ChatBoxView.as_view(), name='chatbox')
]


