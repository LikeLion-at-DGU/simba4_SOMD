from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('',mainpage, name="mainpage"),
    path('test/',test,name="test"),
]