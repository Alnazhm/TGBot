from django.urls import path
from .views import UserRegistrationView, UserLoginView, SendMessageView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('sendmessage/', SendMessageView.as_view(), name='sendmessage'),
]