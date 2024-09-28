from django.urls import path
from workspaces.views import (
    CreateWorkspaceView,
    UserWorkspaceListView,
)    

urlpatterns = [
    path('create/', CreateWorkspaceView.as_view(), name='create'),   
    path('list/', UserWorkspaceListView.as_view(), name='list-workspace'), 
]