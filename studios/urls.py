from django.urls import path
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.neworder, name='new-order'),
    path('create-application/', views.create_application, name='create_application'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('delete-application/<int:pk>/', views.delete_application, name='delete_application'),

    path('login/', CustomLoginView.as_view(), name='login'),
 
]