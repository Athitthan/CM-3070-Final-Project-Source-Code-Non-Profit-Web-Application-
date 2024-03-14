from django.contrib import admin
from .models import *

# Register your models here.


# ---I WROTE THIS CODE---
@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email","group", "background_image", "profile_image", "bio")
    # Add more customizations as needed


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("post_media", "appuser", "created_at")
    # Add more customizations as needed


@admin.register(Followings)
class FollowingsAdmin(admin.ModelAdmin):
    list_display = ("current_user", "following")
    # Add more customizations as needed


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("requested_user", "requester")
    # Add more customizations as needed


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("status", "appuser", "created_at")
    # Add more customizations as needed


@admin.register(ChatMessage)
class CharMessageAdmin(admin.ModelAdmin):
    list_display = ("room_name", "sender", "receiver", "message", "timestamp")
    # Add more customizations as needed

    # ---END OF CODE THAT I WROTE---


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "content", "category", "creator", "created_at")
    # Add more customizations as needed


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "content", "creator", "created_at")
    # Add more customizations as needed


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("comment", "content", "creator", "created_at")
    # Add more customizations as needed


@admin.register(VolunteerHelp)
class VolunteerHelpAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "description",
        "preferred_date_time",
        "duration",
        "location",
        "category",
        "volunteer_limit",
        "created_at",
    )
    # Add more customizations as needed


@admin.register(VolunteeredHelp)
class VolunteeredHelpAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "volunteer_help",
        "created_at",
        "preferred_date_time_field_changed",
        "location_field_changed",
        "title_field_changed",
        "description_field_changed",
        "duration_field_changed",
        "volunteer_limit_field_changed",
    )
    # Add more customizations as needed


@admin.register(DiseaseOverview)
class DiseaseOverviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "image",
    )
    # Add more customizations as needed


@admin.register(ResearchUpdate)
class ResearchUpdateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "summary",
        "publication_date",
        "link",
        "image",
    )
    # Add more customizations as needed


@admin.register(PatientStory)
class PatientStoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "story",
        "date_shared",
        "image",
    )
    # Add more customizations as needed
