from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from workspaces.views.workspace import (
    WorkspaceViewSet,
)
from workspaces.views.category import (
    CategoryViewSet,
)
from workspaces.views.channel import (
    ChannelViewSet
)
from workspaces.views.assignment import (
    AssignmentView
)
from workspaces.views.submission import (
    SubmissionRevieweeView,
    SubmissionReviewerView,
)
from workspaces.views.iteration import (
    IterationCreateView
)

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspaces')

workspaces_router = routers.NestedDefaultRouter(router, r'workspaces', lookup='workspace')
workspaces_router.register(r'categories', CategoryViewSet, basename='workspace-categories')

categories_router = routers.NestedDefaultRouter(workspaces_router, r'categories', lookup='category')
categories_router.register(r'channels', ChannelViewSet, basename='category-channels')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(workspaces_router.urls)),
    path('api/', include(categories_router.urls)),
    path(
        'api/assignment/<uuid:workspace_pk>/<uuid:id>/',
        AssignmentView.as_view(), 
        name="assignment"
    ),
    path(
        'channels/<int:id>/submissions/reviewee/', 
        SubmissionRevieweeView.as_view(), 
        name='submission-reviewee'
    ),
    path(
        'submissions/<int:workspace_pk>/<int:id>/', 
        SubmissionReviewerView.as_view(), 
        name='submission-reviewer'
    ),
    path(
        'submissions/<int:workspace_pk>/<int:id>/<int:user_id>/', 
        SubmissionReviewerView.as_view(), 
        name='submission-reviewer-user'
    ),
    path(
        'iterations/<int:submission_id>/create/', 
        IterationCreateView.as_view(), 
        name='iteration-create'
    ),
]