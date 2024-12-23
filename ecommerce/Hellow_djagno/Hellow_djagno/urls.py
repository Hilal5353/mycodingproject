from django.urls import path, include
from app import urls
from django.contrib import admin

urlpatterns = [
    path('', include(urls), name='homePAGE'),
    path('admin/', admin.site.urls),

]












