from django.urls import path
from django.contrib.auth import views as auth_view
from django.contrib import admin
from core import views
from core.forms import Login

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('update/<str:name>', views.update, name='update'),
    path('process/', views.progres, name='process'),
    path('admin/', admin.site.urls),
    path('delete/<str:name>', views.delete, name='delete'),
    path('logout/', views.logout_view, name='logout'),
]
   









