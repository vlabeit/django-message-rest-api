from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/', include('message_app.urls'), name="api"),
    path('', lambda request: redirect('api/'), name='redirect_to_api'),

]
