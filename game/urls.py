from django.urls import include, path

from . import views

app_name = "game"  # dev_3

urlpatterns = [
    path("rsp/", views.rsp, name="rsp"),  # dev_3 : 가위바위보
    path("lotto/", views.lotto, name="lotto"),  # dev_4 : 로또
]
