from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, activate_user

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('confirm/<str:token>', activate_user, name='confirm'),
    #TODO: написать метод сброса пароля
    # path('resetpassword/', reset_password, name='reset_password'),
]
