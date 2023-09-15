from rest_framework import serializers
from .models import *

#---I WROTE THIS CODE---

# Serializer for listing User model data
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
#---END OF THE CODE THAT I WROTE---        

#---I WROTE THIS CODE---
# Serializer for listing AppUser model data, including related User data
class AppUserListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = AppUser
        fields = ['id', 'name', 'email', 'profile_image', 'background_image', 'bio', 'user']
#---END OF THE CODE THAT I WROTE---        

#---I WROTE THIS CODE---
# Serializer for Followings model
class FollowingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followings
        fields = '__all__'
#---END OF THE CODE THAT I WROTE---        

#---I WROTE THIS CODE---
# Serializer for checking if a row exists
class RowExistsSerializer(serializers.Serializer):
    exists = serializers.BooleanField()
#---END OF THE CODE THAT I WROTE---    

#---I WROTE THIS CODE---
# Serializer for listing friends (Followings model) data
class FriendListSerializer(serializers.ModelSerializer):
    current_user = AppUserListSerializer()
    following = AppUserListSerializer()

    class Meta:
        model = Followings
        fields = ['current_user', 'following']
#---END OF THE CODE THAT I WROTE---        

#---I WROTE THIS CODE---
# Serializer for listing Gallery model data
class GalleryListSerializer(serializers.ModelSerializer):
    appuser = AppUserListSerializer()

    class Meta:
        model = Gallery
        fields = ['id', 'post_image', 'description', 'likes', 'created_at', 'appuser']
#---END OF THE CODE THAT I WROTE---        

#---I WROTE THIS CODE---
# Serializer for creating Gallery model instances
class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['post_image', 'description', 'appuser']
#---END OF THE CODE THAT I WROTE---        

#---I WROTE THIS CODE---
# Serializer for updating the 'likes' field of Gallery model instances
class UpdateLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['likes']
#---END OF THE CODE THAT I WROTE---        

#---I WROTE THIS CODE---
# Serializer for listing Status model data
class StatusListSerializer(serializers.ModelSerializer):
    appuser = AppUserListSerializer()

    class Meta:
        model = Status
        fields = ['id', 'status', 'created_at', 'appuser']

#---END OF THE CODE THAT I WROTE---