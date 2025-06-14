
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('most-liked/', views.most_liked, name='most_liked'),
    path('search/', views.search, name='search'),
    path('most-trending/', views.most_trending, name='most_trending'),
    path('following/', views.following, name='following'),
    path('editprofile/', views.edit_profile, name='editprofile'),
    path('settings/', views.settings, name='settings'),
    path('cratepost/', views.create_post, name='create'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('changepassword', views.changepassword, name='chnagepassword'),
    path('crated_comment/<str:post_id>', views.create_comment, name='create_comment'),
    path('like-post/', views.like_post, name='like-post'),
    path('follow', views.follow, name='follow'),
    path('delete/<str:pk>', views.delete_post, name='delete'),
    path('report/<str:post_id>', views.report, name='report'),
]

