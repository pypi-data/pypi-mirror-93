from django_email_verification import urls as mail_urls
from django.contrib import admin
from django_paperlayer.api.views.rating import RatingViewSet
from django_paperlayer.api.views.comment import CommentViewSet
from django.contrib.auth import views as auth_views
from django_paperlayer.api.views.search import SearchGenericAPIView
from django_paperlayer.api.views.notification import NotificationViewSet
from django_paperlayer.api.views.publication import PublicationViewSet
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from django_paperlayer.api.views.feed import FeedViewSet
from django_paperlayer.api.views.following import FollowingViewSet, FollowRequestViewSet
from django_paperlayer.api.views.profile import ProfileViewSet, ProfilePictureViewSet
from django_paperlayer.api.views.auth import RegisterGenericAPIView, LogoutGenericAPIView, AuthView
from django_paperlayer.api.views.project import ProjectViewSet
from django_paperlayer.api.views.milestone import MilestoneViewSet
from django_paperlayer.api.views.tag import TagViewSet
from django_paperlayer.api.views.user import UserViewSet
from django_paperlayer.api.views.event import EventViewSet
from django_paperlayer.api.views.file import FileViewSet
from django_paperlayer.api.views.collaboration_request import CollaborationRequestViewSet
from django_paperlayer.api.views.collaboration_invite import CollaborationInviteViewSet
from django_paperlayer.api.views.report import ReportViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'profile_picture', ProfilePictureViewSet)
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'milestones', MilestoneViewSet)
router.register(r'tags', TagViewSet)
router.register(r'events', EventViewSet)
router.register(r'files', FileViewSet)
router.register(r'follow', FollowingViewSet)
router.register(r'follow_request', FollowRequestViewSet)
router.register(r'collaboration_requests', CollaborationRequestViewSet)
router.register(r'collaboration_invites', CollaborationInviteViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'comments', CommentViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'feeds', FeedViewSet, basename='feed')
router.register(r'publications', PublicationViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterGenericAPIView.as_view()),
    path('auth/', AuthView.as_view(), name='auth'),
    path('logout/', LogoutGenericAPIView.as_view()),
    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path('admin/', admin.site.urls),
    path('email/', include(mail_urls)),
    path('search/', SearchGenericAPIView.as_view(), name='search'),

]
