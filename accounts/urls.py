from django.urls import path
from . import views

urlpatterns = [
  path("register/",views.register,name="register"),
  path('activate/<uidb64>/<token>/',views.activate,name='activate'),
  path('forgot_password/',views.forgot_password,name='forgot_password'),
  path('reset_validate/<uidb64>/<token>/',views.reset_validate,name='reset_validate'),
  path('reset_password/',views.reset_password,name='reset_password'),
  path("login/",views.login,name="login"),
  path("logout_view/",views.logout_view,name="logout_view"),
]
