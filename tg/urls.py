from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.ChatList.as_view(), name="chat_list"),
    path("chat/<int:pk>", views.ChatDetail.as_view(), name="chat_detail"),
]