from django.urls import path
from taskapp.views import TaskView

urlpatterns = [
    path('get/<str:tid>', TaskView.as_view(), name="get-task-view"),
    path('<str:action>', TaskView.as_view(), name="post-task-view"),
]

