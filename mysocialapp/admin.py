from django.contrib import admin
from .models import *

# Register your models here.


#---I WROTE THIS CODE---
@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'name','email','background_image','profile_image','bio')
    # Add more customizations as needed

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('post_image', 'appuser','created_at')
    # Add more customizations as needed



@admin.register(Followings)
class FollowingsAdmin(admin.ModelAdmin):
    list_display = ('current_user','following')
    # Add more customizations as needed



@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'appuser','created_at')
    # Add more customizations as needed

@admin.register(ChatMessage)
class CharMessageAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'sender','message','timestamp')
    # Add more customizations as needed

    #---END OF CODE THAT I WROTE---