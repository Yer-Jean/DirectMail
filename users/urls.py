from django.contrib.auth.views import  LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, activate_user, UserUpdateView, UserLoginView, UserListView, toggle_active, \
    password_reset

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('confirm/<str:token>', activate_user, name='confirm'),
    path('users/', UserListView.as_view(), name='users'),
    path('toggle_active/<int:pk>', toggle_active, name='toggle_active'),
    path('password_reset/', password_reset, name='password_reset'),
]
