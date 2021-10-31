from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eye/', include('eye.urls', namespace='eye')),
    path('token-auth/',views.obtain_auth_token,name='token-auth'),
]
