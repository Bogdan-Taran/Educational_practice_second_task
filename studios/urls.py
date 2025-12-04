from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('', views.neworder, name='new-order'),
    path('create-application/', views.create_application, name='create_application'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('delete-application/<int:pk>/', views.delete_application, name='delete_application'),
 
]