from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studios/', include('studios.urls')),
    path('accounts/', include('django.contrib.auth.urls')), #путь для auth
    
    path('', RedirectView.as_view(url='/studios/', permanent=True)),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
