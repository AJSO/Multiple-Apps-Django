from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import sent, activate, register, index, auth_login, user_settings, logout_view

urlpatterns = [
    path('', register, name="register"),
    path('sent/', sent, name='account_activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('dashboard/', index, name="dashboard"),
     path('settings/', user_settings, name="user_settings"),
    path('signin/', auth_login, name="login"),
    path('logout/',logout_view, name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

