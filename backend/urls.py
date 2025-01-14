"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings  # type: ignore          
from django.contrib import admin  # type: ignore          
from django.urls import path, include  # type: ignore          
from django.conf.urls.static import static  # type: ignore          
from users.views import (
    CreateResetPassword,
    ConfirmeResetPassword
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app.urls")),
    
    path("api/v0/auth/", include("dj_rest_auth.urls")),
    path("api/v0/auth/registration/", include("dj_rest_auth.registration.urls")),
    path('api/v0/auth/reset_password/', CreateResetPassword.as_view(), name='create_reset_password'),
    path('api/v0/auth/confirm_reset_password/', ConfirmeResetPassword.as_view(), name='confirm_reset_password'),
    # path(r"api/v0/auth/", include("knox.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
