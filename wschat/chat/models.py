from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatMessagesManager(models.Manager):

    def by_chat(self, chat):
        queryset = Message.objects.filter(chat=chat).order_by("-timestamp")
        return queryset


class Chat(models.Model):
    name = models.CharField(max_length=512, blank=False, null=False, unique=True)
    user = models.ManyToManyField(User, related_name='chats_with_user')
    

class Message(models.Model):
    text = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    received = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    objects = ChatMessagesManager()
