from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name="homepage"),
    path('adduser/',views.register_user,name="register_user"),
    path('loginuser/',views.login_user,name="login_user")
]