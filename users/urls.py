from django.urls import path
from .views import *

app_name = "users"
urlpatterns = [
    path("myPage/", myPage, name="myPage"),
    path("myPage_edit/", myPage_edit, name="myPage_edit"),
    path("myPage_update/", myPage_update, name="myPage_update"),
]
