from rest_framework import serializers
from .models import *

# ---I WROTE THIS CODE---


# Serializer for listing User model data
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


# ---END OF THE CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Serializer for listing AppUser model data, including related User data
class AppUserListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = AppUser
        fields = [
            "id",
            "name",
            "email",
            "profile_image",
            "background_image",
            "bio",
            "user",
        ]


# ---END OF THE CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Serializer for Followings model
class FollowingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followings
        fields = "__all__"


# ---END OF THE CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Serializer for checking if a row exists
class RowExistsSerializer(serializers.Serializer):
    exists = serializers.BooleanField()


# ---END OF THE CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Serializer for listing friends (Followings model) data
class FriendListSerializer(serializers.ModelSerializer):
    current_user = AppUserListSerializer()
    following = AppUserListSerializer()

    class Meta:
        model = Followings
        fields = ["current_user", "following"]


# ---END OF THE CODE THAT I WROTE---


# Serializer for listing requests (Request model) data
class RequestListSerializer(serializers.ModelSerializer):
    requested_user = AppUserListSerializer()
    requester = AppUserListSerializer()

    class Meta:
        model = Request
        fields = ["requested_user", "requester"]


# ---I WROTE THIS CODE---
# Serializer for listing Gallery model data
class GalleryListSerializer(serializers.ModelSerializer):
    appuser = AppUserListSerializer()

    class Meta:
        model = Gallery
        fields = [
            "id",
            "post_media",
            "description",
            "likes",
            "created_at",
            "appuser",
        ]


# ---END OF THE CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Serializer for creating Gallery model instances
class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["post_media", "description", "appuser"]


# ---END OF THE CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Serializer for updating the 'likes' field of Gallery model instances
class UpdateLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["likes"]


# ---END OF THE CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Serializer for listing Status model data
class StatusListSerializer(serializers.ModelSerializer):
    appuser = AppUserListSerializer()

    class Meta:
        model = Status
        fields = ["id", "status", "created_at", "appuser"]


# ---END OF THE CODE THAT I WROTE---


class ForumCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "creator", "content", "created_at")


class ForumReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ("id", "comment", "creator", "content", "created_at")


class CommitToVolunteerHelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteeredHelp  # Use the appropriate model
        fields = [
            "volunteer_help",
            "user",
        ]  # Specify fields you want from the POST request


class DiseaseOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseOverview
        fields = ["id", "title"]


class ResearchUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchUpdate
        fields = ["id", "title"]


class PatientStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientStory
        fields = ["id", "title"]
