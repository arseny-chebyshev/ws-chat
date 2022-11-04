from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import ChatForm
from .models import Chat, Message
# Create your views here.

class ChatBoxView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request, chat_box_name):
        return render(request, "chat/chatbox.html", context={"chat_box_name": chat_box_name,
                                                            "messages": Message.objects.filter(
                                                            chat=Chat.objects.get(name=chat_box_name))})

class ChatView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request):
        chat_form = ChatForm()
        context = {"chats": Chat.objects.all(), "chat_form": chat_form}
        return render(request, 'chat/main.html', context=context)

    def post(self, request):
        user = request.user
        new_chat = Chat.objects.get_or_create(name=request.POST['name'])[0]
        new_chat.user.add(user)
        new_chat.save()
        return redirect(reverse(f'chat:chatbox', args=(new_chat.name, )))
