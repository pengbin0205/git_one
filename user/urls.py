from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path("register/", views.register, name='register'),
    path("user_register/", views.user_register, name="user_register"),
    path("send_email/", views.send_email, name="send_email"),
    path("login/", views.login, name="login"),
    path("login2/", views.login2, name="login2"),
    path("captcha/", views.captcha, name="captcha"),
    path("ce2/", views.checkEmail2, name="ce2"),
    path("checkEmail2/", views.checkEmail2, name="checkEmail2"),
    path("checkPhone2/", views.checkPhone2, name="checkPhone2"),
]