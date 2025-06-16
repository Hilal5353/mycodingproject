from app import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:group_name>/', views.home, name='home'), 
]
