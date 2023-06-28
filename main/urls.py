from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('',start,name="start"),
    path('mainPage',mainPage, name="mainPage"),
    path('somdList/',somdList,name="somdList"),
    path('somd_new/',somd_new,name="somd_new"),
    path('somd_edit/<int:id>', somd_edit, name="somd_edit"),
    path("somd_update/<int:id>", somd_update, name="somd_update"),

    path('mySomd/',mySomd,name="mySomd"),
    path('somd_create/',somd_create,name="somd_create"),
    path('somdFeed/<int:id>/',somdFeed,name="somdFeed"),
    # path('somdFeed/<int:id>/',postContainer_change,name="postContainer_change"),
    
    path('fix/<int:post_id>/<int:somd_id>/', fix, name="fix"),
    
    path('somdFeed/<int:somd_id>/somd_post_new/',somd_post_new, name="somd_post_new"),
    path('somdFeed/<int:somd_id>/somd_post_create/',somd_post_create,name="somd_post_create"),
    
    path('somdFeed/somd_post_view/<int:post_id>/',somd_post_view,name="somd_post_view"),
    path('somdFeed/somd_post_edit/<int:post_id>/', somd_post_edit, name="somd_post_edit"),
    path('somdFeed/somd_post_update/<int:post_id>/',somd_post_update,name="somd_post_update"),
    path('somdFeed/somd_post_delete/<int:post_id>/',somd_post_delete,name="somd_post_delete"),
    path('somdFeed/comment_update/<int:post_id>/<int:comment_id>/',comment_update,name="comment_update"),
    path('somdFeed/comment_delete/<int:post_id>/<int:comment_id>/',comment_delete,name="comment_delete"),

    
    path('scrap/<int:post_id>/',scrap,name="scrap"),
    path('scrap_view/',scrap_view,name="scrap_view"),

    path('like/<int:post_id>/',somd_post_like,name="somd_post_like"),
    path('like/<int:post_id>/',somd_post_like,name="somd_post_like"),
    path('bookmark/<int:somd_id>/',bookmark,name="bookmark"),
    path('join/<int:id>/', join, name="join"),
    path('wantTojoin/<int:id>/', wantTojoin, name= 'wantTojoin'),
    
    path('somd_members/<int:id>/',somd_members,name="somd_members"),
    path('somd_members_wantTojoin/<int:somd_id>/<int:request_id>/',somd_members_wantTojoin,name="somd_members_wantTojoin"),
    path('somd_members_delete/<int:somd_id>/<int:join_user_id>/',somd_members_delete,name="somd_members_delete"),
    
    path('alram/',alram,name="alram"),
]
