from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users/', include('users.urls')),
    path('', include('features.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


