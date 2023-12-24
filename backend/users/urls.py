from django.urls import include, path

from rest_framework import routers

from .views import OAuthViewset, EmailValidationConfirmView, RegisterView


router = routers.DefaultRouter()
router.register(r'', OAuthViewset, basename='google')

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path(
        'email-validation/confirm/',
        EmailValidationConfirmView.as_view(),
        name='email_validation_confirm',
    ),
    path('', include(router.urls)),
]
