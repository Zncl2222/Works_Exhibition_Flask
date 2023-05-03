from django.urls import path

from .views import EmailValidationView, EmailValidationConfirmView, RegisterView


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('email-validation/', EmailValidationView.as_view(), name='email_validation'),
    path(
        'email-validation/confirm/',
        EmailValidationConfirmView.as_view(),
        name='email_validation_confirm',
    ),
]
