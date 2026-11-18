from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    RegisterView,
    TaskListCreateView,
    TaskDetailView
)


urlpatterns = [

    path('register/', RegisterView.as_view()),

    path('login/', obtain_auth_token),

    path('tasks/', TaskListCreateView.as_view()),

    path('tasks/<int:pk>/', TaskDetailView.as_view()),

]