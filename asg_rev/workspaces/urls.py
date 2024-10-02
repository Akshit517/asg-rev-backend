from django.urls import path, include
from rest_framework.routers import DefaultRouter
from workspaces.views.workspace import (
    WorkspaceViewSet,
)

router = DefaultRouter()
router.register(r'workspace', WorkspaceViewSet, basename='workspace')


urlpatterns = [
    path('', include(router.urls)),
]