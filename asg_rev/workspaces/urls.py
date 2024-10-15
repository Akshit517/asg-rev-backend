from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from workspaces.views.workspace import (
    WorkspaceViewSet,
    WorkspaceMemberView,
    WorkspaceMemberDetailView,
)
from workspaces.views.category import (
    CategoryViewSet,
    CategoryMemberView,
    CategoryMemberDetailView
)
from workspaces.views.channel import (
    ChannelViewSet,
    ChannelMemberView,
    ChannelMemberDetailView
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

prefix_url = 'api/'

urlpatterns = [
    path(f'{prefix_url}', include(router.urls)),
    path(f'{prefix_url}', include(workspaces_router.urls)),
    path(f'{prefix_url}', include(categories_router.urls)),
    path(
        f'{prefix_url}workspaces/<uuid:workspace_pk>/members/', 
        WorkspaceMemberView.as_view(), 
        name='workspace-member'
    ),
    path(
        f'{prefix_url}workspaces/<uuid:workspace_pk>/members/detail/', 
        WorkspaceMemberDetailView.as_view(), 
        name='workspace-member-detail'
    ),
    path(
        f'{prefix_url}workspaces/<uuid:workspace_pk>/categories/<int:category_pk>/members/', 
        CategoryMemberView.as_view(), 
        name='category-member-list-create'
    ),
    path(
        f'{prefix_url}workspaces/<uuid:workspace_pk>/categories/<int:category_pk>/members/detail/', 
        CategoryMemberDetailView.as_view(), 
        name='category-member-detail'
    ),
    path(
        f'{prefix_url}workspaces/<uuid:workspace_pk>/categories/<int:category_pk>/channels/<uuid:channel_pk>/members/', 
        ChannelMemberView.as_view(), 
        name='category-member-list-create'
    ),
    path(
        f'{prefix_url}workspaces/<uuid:workspace_pk>/categories/<int:category_pk>/channels/<uuid:channel_pk>/members/detail/', 
        ChannelMemberDetailView.as_view(), 
        name='category-member-detail'
    ),
    path(
        f'{prefix_url}workspaces/<uuid:workspace_pk>/<uuid:id>/assignment/',
        AssignmentView.as_view(), 
        name="assignment"
    ),
    path(
        f'{prefix_url}<uuid:workspace_pk>/<uuid:id>/submissions/reviewee/', 
        SubmissionRevieweeView.as_view(), 
        name='submission-reviewee'
    ),
    path(
        f'{prefix_url}<uuid:workspace_pk>/<uuid:id>/submissions/reviewer/', 
        SubmissionReviewerView.as_view(), 
        name='submission-reviewer'
    ),
    path(
        f'{prefix_url}<uuid:workspace_pk>/<uuid:id>/submissions/<int:user_id>/', 
        SubmissionReviewerView.as_view(), 
        name='submission-reviewer-user'
    ),
    path(
        f'{prefix_url}<int:submission_id>/iterations/create/', 
        IterationCreateView.as_view(), 
        name='iteration-create'
    ),
]