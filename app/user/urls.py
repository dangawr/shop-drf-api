from django.urls import path, include
from .views import CreateUserApiView, CustomAuthToken, UpdateUserDetailsApiView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserApiView.as_view(), name='create'),
    path('token/', CustomAuthToken.as_view(), name='token'),
    path('me/', UpdateUserDetailsApiView.as_view(), name='me'),
]
