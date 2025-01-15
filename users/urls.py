from django.urls import path, include          
from django.conf.urls.static import static          
from users.views import (
    CreateResetPassword,
    ConfirmeResetPassword
)

urlpatterns = [
    path("api/v0/auth/", include("dj_rest_auth.urls")),
    path("api/v0/auth/registration/", include("dj_rest_auth.registration.urls")),
    path('api/v0/auth/reset_password/', CreateResetPassword.as_view(), name='create_reset_password'),
    path('api/v0/auth/confirm_reset_password/', ConfirmeResetPassword.as_view(), name='confirm_reset_password'),
]
