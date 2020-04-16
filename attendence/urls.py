from django.urls import path, include
from user.views import user_settings
from django.conf import settings 
from django.conf.urls.static import static 

from .views import create_leave

urlpatterns = [
    path('leaveApplication/', create_leave, name='create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
