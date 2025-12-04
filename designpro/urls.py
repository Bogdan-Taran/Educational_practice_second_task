from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from studios.views import registration
from studios import views as studios_views

urlpatterns = [
    path('superadmin/', admin.site.urls,),
    path('admin/', RedirectView.as_view(url='/superadmin/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')), 

    path('user/registration/', registration, name='signup'),
    path('studios/', include('studios.urls')),
    
    path('', RedirectView.as_view(url='/studios/', permanent=True)),


    path('admin/applications/', studios_views.admin_applications, name='admin_applications'),
    path('admin/applications/<int:pk>/change-status/', studios_views.change_application_status, name='change_application_status'),
    path('admin/categories/', studios_views.manage_categories, name='manage_categories'),
    path('admin/categories/<int:pk>/delete/', studios_views.delete_category, name='delete_category'),
    path('admin/categories/add/', studios_views.add_category, name='add_category'),
    
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
