from django.contrib import admin
from .models import Chat, Group
# Register your models here.

@admin.register(Chat)
class MyChat(admin.ModelAdmin):
    list_display = ['id', 'content', 'timestamp', 'group']
    
@admin.register(Group)
class MyGroup(admin.ModelAdmin):
    list_display = ['id', 'name']