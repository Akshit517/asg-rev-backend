from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from workspaces.views import (
    WorkspaceViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspaces')

workspaces_router = routers.NestedDefaultRouter(router, r'workspaces', lookup='workspace')
workspaces_router.register(r'categories', CategoryViewSet, basename='workspace-categories')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(workspaces_router.urls)),
]