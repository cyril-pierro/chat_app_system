from django.urls import path

from search import views

urlpatterns = [
    path("user/<str:username>", views.SearchUsers.as_view()),
]
