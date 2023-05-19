from django.urls import path
from search import views

app_name = "search"

urlpatterns = [
    path("user/<str:username>", views.SearchUsers.as_view(), name="search_user"),
    path("users/", views.AllUsers.as_view(), name="get_all_users"),
]
