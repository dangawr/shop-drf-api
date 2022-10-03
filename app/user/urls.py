from django.urls import path, include
from .views import CreateUserApiView, CustomAuthToken, UpdateUserDetailsApiView, LogOutUserApiView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserApiView.as_view(), name='create'),
    path('token/', CustomAuthToken.as_view(), name='token'),
    path('me/', UpdateUserDetailsApiView.as_view(), name='me'),
    path('logout/', LogOutUserApiView.as_view(), name='logout'),
]
