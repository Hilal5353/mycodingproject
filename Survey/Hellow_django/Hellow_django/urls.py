from django.urls import path
from django.contrib import admin
from home import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('survey/<str:id>/', views.customer_feedback, name='feedback'),
    path('thankyou/', views.thankyou, name='thankyou'),
]
