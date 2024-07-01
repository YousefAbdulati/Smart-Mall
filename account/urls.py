from django.urls import path
from account.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserPasswordResetView
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profiles/', UserProfileView.as_view(), name='profile'),
    path('profiles/<int:pk>/', UserProfileView.as_view(), name='profile-detail'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
]