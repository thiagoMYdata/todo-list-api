from django.urls import path, re_path
from . import views

urlpatterns = [
    path("api/", views.taskList, name="main"),
    re_path("login", views.login),
    re_path("signup", views.signup),
    re_path("tasks", views.getAllTask),
    re_path("create-task", views.postNewTask),


]
