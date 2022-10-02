from django.urls import path, include
from .views import CreateUserApiView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserApiView.as_view(), name='create')
]
