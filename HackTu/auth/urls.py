from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.register, name="register"),
    path("login/", views.handlelogin, name="handlelogin"),
    path("logout/", views.handlelogout, name="handlelogout"),
    path(
        "activate/<uidb64>/<token>",
        views.ActivateAccountView.as_view(),
        name="activate",
    ),
]
