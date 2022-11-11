from django.urls import path

from users.views import CustomUserView


app_name = 'users'

urlpatterns = [
    path('register/', CustomUserView.as_view(), name='create_user')
]
