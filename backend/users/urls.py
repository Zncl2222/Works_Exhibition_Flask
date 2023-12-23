from django.urls import path

from .views import EmailValidationConfirmView, RegisterView


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path(
        'email-validation/confirm/',
        EmailValidationConfirmView.as_view(),
        name='email_validation_confirm',
    ),
]
