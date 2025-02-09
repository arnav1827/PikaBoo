from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("jee/", views.jee, name="jee"),
    path("master/", views.master, name="master"),
    path("masterdashboard/", views.masterdashboard, name="masterdashboard"),
    path("profile/", views.profile, name="profile"),
    path("assistance/", views.assistance, name="assistance"),
    path("reports/", views.reports, name="reports"),
    path("analysis/", views.analysis, name="analysis"),
]
