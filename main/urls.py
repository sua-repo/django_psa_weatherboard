from django.contrib import admin
from django.urls import include, path
from . import views

app_name="main"

urlpatterns = [
    path("", views.index, name="index"),     # dev_2 : 홈화면 

]
