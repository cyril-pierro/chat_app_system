from django.urls import path
from search import views

app_name = "search"

urlpatterns = [
    path("user/<str:username>", views.SearchUsers.as_view(), name="user"),
    path("users/", views.AllUsers.as_view(), name="users"),
]
