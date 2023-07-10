from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_survey", views.new_survey, name="new_survey"),
    path("surveys", views.surveys, name="surveys"),
    path("profile", views.profile, name="profile"),
    path("results", views.results, name="results")
]
