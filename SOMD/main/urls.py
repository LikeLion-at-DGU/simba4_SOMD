from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('',mainpage, name="mainpage"),
    path('board/',board,name="board"),
    path('register/',register,name="register"),
    path('somd_edit/<int:id>', somd_edit, name="somd_edit"),
    path("somd_update/<int:id>", somd_update, name="somd_update"),

    path('mysomd/',mysomd,name="mysomd"),
    path('createSOMD/',createSOMD,name="createSOMD"),
    path('mainfeed/<int:id>',mainfeed,name="mainfeed"),
    path('fix/<int:post_id>/<int:somd_id>/', fix, name="fix"),
    
    path('mainfeed/<int:somd_id>/new/',new, name="new"),
    path('mainfeed/<int:somd_id>/createpost/',createpost,name="createpost"),
    path('mainfeed/viewpost/<int:post_id>',viewpost,name="viewpost"),
    
    path('join/<int:id>', join, name="join"),
    path('wantTojoin/<int:id>', wantTojoin, name= 'wantTojoin'),
    
    path('members/<int:id>',members,name="members"),
    path('members_wantTojoin/<int:somd_id>/<int:request_id>',members_wantTojoin,name="members_wantTojoin"),
    path('members_delete/<int:somd_id>/<int:join_user_id>',members_delete,name="members_delete"),
]
