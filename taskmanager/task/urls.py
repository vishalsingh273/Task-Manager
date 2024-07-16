from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    TaskListCreateView,
    TaskDetailView,
    TaskMemberView,
    UpdateTaskStatusView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/members/', TaskMemberView.as_view(), name='task-members'),
    path('tasks/<int:pk>/members/<int:user_id>/', TaskMemberView.as_view(), name='task-member-manage'),
    path('tasks/<int:pk>/status/', UpdateTaskStatusView.as_view(), name='task-status-update'),
]
