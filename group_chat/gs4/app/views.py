from django.shortcuts import render
from .models import Group, Chat
# Create your views here.

def home(request, group_name):
    group = Group.objects.filter(name = group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        group = Group(name = group_name)
        group.save()
    print("your group name", group_name)
    return render(request, 'app/index.html', {'groupname':group_name, 'chats':chats})