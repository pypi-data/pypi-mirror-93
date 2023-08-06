from django.contrib import admin

# Register your models here.
from django_paperlayer.api.models.following import Following, FollowRequest
from django_paperlayer.api.models.profile import Profile
from django_paperlayer.api.models.project import Project
from django_paperlayer.api.models.event import Event
from django_paperlayer.api.models.file import File
from django_paperlayer.api.models.notification import Notification
from django_paperlayer.api.models.collaboration_invite import CollaborationInvite
from django_paperlayer.api.models.collaboration_request import CollaborationRequest
from django_paperlayer.api.models.comment import Comment
from django_paperlayer.api.models.rating import Rating
from django_paperlayer.api.models.tag import Tag
from django_paperlayer.api.models.report import Report

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Event)
admin.site.register(File)
admin.site.register(Following)
admin.site.register(FollowRequest)
admin.site.register(Notification)
admin.site.register(CollaborationInvite)
admin.site.register(CollaborationRequest)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Tag)
admin.site.register(Report)
