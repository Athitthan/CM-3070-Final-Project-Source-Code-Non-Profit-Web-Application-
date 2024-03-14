from django.utils import timezone
import os
from typing import Any, Dict, List, Optional
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django import forms
from .models import *
from .form import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# ---I WROTE THIS CODE---


@login_required
def userDetailsApi(request, id):
    appuser = AppUser.objects.get(id=id)

    return render(request, "screens/userDetailsApi.html", {"appuser": appuser})


# --- END OF CODE THAT I WROTE---


# Create your views here.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("../")


# Render about us page.
def aboutUs(request):
    return render(request, "screens/about_us.html")


# This view handles user login.
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("./profile")  # Redirect to a success page
            else:
                return HttpResponse("Your account is disabled.")

        else:
            form = UserLoginForm()
            return render(
                request,
                "screens/login.html",
                {"form": form, "error": "Invalid login details"},
            )

    else:
        form = UserLoginForm()
    # If it's a GET request or if authentication failed, render the login page with the form
    return render(request, "screens/login.html", {"form": form})


# This view handles user registration.
def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if "email" in user_form.cleaned_data:
                profile.email = request.POST["email"]

            profile.save()
            Status.objects.create(appuser=profile)
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "screens/register.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


# ---I WROTE THIS CODE---


# This view displays the user's homepage.
@login_required
def profile(request):
    user = request.user  # Get the authenticated user
    context = {"user": user}
    appuser = AppUser.objects.get(user=user)
    print(appuser.name)
    return render(request, "screens/profile.html", {"user": user, "appuser": appuser})


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# This view allows users to update their profile
class UserProfileUpdate(UpdateView):
    model = AppUser
    fields = ["name", "email", "profile_image", "background_image", "bio"]
    template_name = "screens/update_user_profile.html"

    def get_success_url(self):
        return reverse_lazy("profile")

    def form_valid(self, form):
        # Get the current instance of AppUser
        app_user = AppUser.objects.get(id=self.kwargs["pk"])

        # Save the form and return the response
        return super().form_valid(form)


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# This view displays the user's homepage for a specific contact.
@login_required
def userProfile(request, contact_username):
    user = request.user  # Get the authenticated user
    context = {"user": user}
    appuser = AppUser.objects.get(user=user)
    contact = AppUser.objects.get(user__username=contact_username)
    print(appuser.name)
    return render(
        request,
        "screens/profile.html",
        {"user": user, "appuser": appuser, "contact": contact},
    )


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# This view allows users to follow or unfollow other users.
@login_required
def follow(request):
    user = request.user
    appuser = AppUser.objects.get(user=user)

    if request.method == "GET":
        following = request.GET.get("following")
        path = request.GET.get("path")
        contact = AppUser.objects.get(user__username=following)
        instance1, created1 = Followings.objects.get_or_create(
            current_user=appuser, following=contact
        )
        instance2, created2 = Followings.objects.get_or_create(
            current_user=contact, following=appuser
        )

        if created1 and created2:
            if Request.objects.filter(requester=contact).exists:
                Request.objects.get(requester=contact).delete()
            if Request.objects.filter(requester=appuser).exists():
                Request.objects.get(requester=appuser).delete()

            return HttpResponseRedirect(f"../profile")
        else:
            instance1.delete()
            instance2.delete()
            if path == "profile":
                return HttpResponseRedirect(f"../profile")
            else:
                return HttpResponseRedirect(f"../user_profile/{contact.user.username}")

    else:
        return HttpResponseRedirect("../profile")


# ---END OF CODE THAT I WROTE---


# This view allows users to request or unrequest other users.
@login_required
def request(request):
    # Get the current authenticated user and corresponding AppUser instance.
    user = request.user
    current_user = AppUser.objects.get(user=user)

    # Only process GET requests to handle friend request actions.
    if request.method == "GET":
        # Retrieve 'requestedUserId' and 'requesterId' from the query parameters.
        requested_user_id = int(request.GET.get("requestedUserId"))
        requester_id = int(request.GET.get("requesterId"))

        # Fetch the AppUser instances for both the requested user and the requester.
        requested_user = AppUser.objects.get(id=requested_user_id)
        requester = AppUser.objects.get(id=requester_id)

        # Attempt to create a new Request instance, or get the existing one if it already exists.
        # 'created1' is True if the Request instance was created, and False if it already existed.
        instance1, created1 = Request.objects.get_or_create(
            requested_user=requested_user, requester=requester
        )

        # If the Request instance was newly created, redirect based on who is the current user.
        if created1:
            # If the current user is the requester, redirect to the requested user's profile.
            if current_user.id == requester_id:
                return HttpResponseRedirect(
                    f"../user_profile/{requested_user.user.username}"
                )
            # If the current user is the requested user, redirect to their own profile.
            elif current_user.id == requested_user_id:
                return HttpResponseRedirect(f"../profile")

        # If the Request instance already existed, it implies a cancellation or rejection of the request,
        # so the instance is deleted.
        else:
            instance1.delete()
            # Redirect the user similarly as above, based on their role (requester or requested).
            if current_user.id == requester_id:
                return HttpResponseRedirect(
                    f"../user_profile/{requested_user.user.username}"
                )
            elif current_user.id == requested_user_id:
                return HttpResponseRedirect(f"../profile")


# ---I WROTE THIS CODE---
# This view allows users to delete a post from their gallery.
@login_required
def deletePost(request, id):
    post = Gallery.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect("../profile#status_container")


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# This view allows users to update their status.
@login_required
def updateStatus(request, id):
    if request.method == "POST":
        statusText = request.POST["statusText"]
        status = Status.objects.get(appuser__id=id)
        status.status = statusText
        status.created_at = timezone.now()
        status.save()

    return HttpResponseRedirect("../profile#status_container")


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# This view sets up a chat room for users to chat with each other.
@login_required
def chatRoom(request, contact_username):
    current_username = request.user.username
    roomName = create_chatroom(current_username, contact_username)

    return render(
        request,
        "screens/chat_room.html",
        {
            "room_name": roomName,
            "username": current_username,
            "contact_username": contact_username,
        },
    )


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# This function creates a chat room name based on the user names.
def create_chatroom(user1, user2):
    # Compare the user strings and arrange them alphabetically
    if user1 < user2:
        chatroom = f"chat_{user1}_{user2}"
    else:
        chatroom = f"chat_{user2}_{user1}"

    return chatroom


# ---END OF CODE THAT I WROTE---


@login_required
def check_unread_messages(request):
    sender_username = request.GET.get("sender_username")
    receiver_username = request.user.username
    
    unread_count = ChatMessage.objects.filter(
        sender=sender_username, receiver=receiver_username, is_read=False
    ).count()

    return JsonResponse({"unread_count": unread_count})


# This view displays the forum page.
@login_required
def forum(request):
    user = request.user  # Get the authenticated user
    appuser = AppUser.objects.get(user=user)

    # Retrieve the selected category from the request's GET parameters
    selected_category = request.GET.get("category")

    # Query all categories
    categories = ["treatment", "emotional", "lifestyle", "challenges"]

    # Query forum posts based on the selected category if available
    if selected_category:
        forum_posts = ForumPost.objects.filter(category=selected_category).order_by(
            "-created_at"
        )
    else:
        forum_posts = ForumPost.objects.filter(category="treatment").order_by(
            "-created_at"
        )

    # Add the count of comments for each forum post to the context
    forum_posts_with_comment_count = []
    for post in forum_posts:
        comment_count = Comment.objects.filter(post=post).count()
        forum_posts_with_comment_count.append((post, comment_count))

    context = {
        "user": user,
        "appuser": appuser,
        "categories": categories,
        "selected_category": selected_category,
        "forum_posts": forum_posts_with_comment_count,
    }

    return render(request, "screens/forum.html", context)


# This view allows users to create a forum post
class CreateForumPost(CreateView):
    model = ForumPost
    fields = ["title", "image", "content", "category"]
    template_name = "screens/create_forum_post.html"

    def get_success_url(self):
        return reverse_lazy("forum")

    def form_valid(self, form):
        # Automatically set the creator field to the current user
        app_user = AppUser.objects.get(user=self.request.user)
        form.instance.creator = app_user
        # Save the form and return the response
        return super().form_valid(form)


# This view allows users to update their forum posts
class UpdateForumPost(UpdateView):
    model = ForumPost
    fields = ["title", "image", "content"]
    template_name = "screens/update_forum_post.html"

    def get_success_url(self):
        return reverse_lazy("forum")

    def form_valid(self, form):
        # Save the form and return the response
        return super().form_valid(form)


# This view allows users to delete a post from their forum.
@login_required
def deleteForumPost(request, id):
    forum_post = ForumPost.objects.get(id=id)
    category = forum_post.category
    forum_post.delete()
    return HttpResponseRedirect(f"../forum/?category={category}")


# This view displays the forum_post_content page.
@login_required
def forumPostContent(request):
    user = request.user  # Get the authenticated user
    appuser = AppUser.objects.get(user=user)

    # Retrieve the selected post from the request's GET parameters
    selected_post_id = request.GET.get("postId")

    # Query comment based on the selected post
    if selected_post_id:
        post = ForumPost.objects.get(id=selected_post_id)
        post_comments = Comment.objects.filter(post=post)
        comment_count = post_comments.count()

    # Add the count of reply for each post comment to the context
    post_comments_with_replies_replyCount = []
    for comment in post_comments:
        replies = Reply.objects.filter(comment=comment)
        reply_count = replies.count()
        post_comments_with_replies_replyCount.append((comment, replies, reply_count))

    context = {
        "user": user,
        "appuser": appuser,
        "post": post,
        "comment_count": comment_count,
        "post_comments": post_comments_with_replies_replyCount,
    }

    return render(request, "screens/forum_post_content.html", context)


@login_required
def userForumPosts(request):
    user = request.user  # Get the authenticated user
    appuser = AppUser.objects.get(user=user)

    # Query all forum posts based on user
    forum_posts = ForumPost.objects.filter(creator=appuser).order_by("-created_at")

    # Add the count of comments for each forum post to the context
    forum_posts_with_comment_count = []
    for post in forum_posts:
        comment_count = Comment.objects.filter(post=post).count()
        forum_posts_with_comment_count.append((post, comment_count))

    context = {
        "user": user,
        "appuser": appuser,
        "forum_posts": forum_posts_with_comment_count,
    }

    return render(request, "screens/user_forum_posts.html", context)


# This view allows users to delete a post comment.
@login_required
def deleteForumPostComment(request, comment_id, post_id):
    post_comment = Comment.objects.get(id=comment_id)
    post_comment.delete()
    return HttpResponseRedirect(
        f"../../forum_post_content/?postId={post_id}#comments_replies_container"
    )


# This view allows users to delete a post reply.
@login_required
def deleteForumPostReply(request, reply_id, post_id):
    post_reply = Reply.objects.get(id=reply_id)
    post_reply.delete()
    return HttpResponseRedirect(
        f"../../forum_post_content/?postId={post_id}#comment_container_{post_reply.comment.id}"
    )


@login_required
def patient_volunteer_helps(request):
    user = request.user  # Get the authenticated user
    appuser = AppUser.objects.get(user=user)
    # Get the current time
    now = timezone.now()

    # Retrieve all VolunteerHelp instances created by the logged-in user where preferred_date_time has not passed
    upcoming_helps = VolunteerHelp.objects.filter(
        user=appuser, preferred_date_time__gt=now
    )

    # Find and delete any VolunteerHelp instances where preferred_date_time is in the past
    past_helps = VolunteerHelp.objects.filter(
        user=appuser, preferred_date_time__lte=now
    )
    # Save a list of titles and categories of past helps before deletion
    expired_helps_info = [
        {"title": help.title, "category": help.get_category_display()}
        for help in past_helps
    ]
    past_helps.delete()

    upcoming_helps_noOfVol_info = []
    for help in upcoming_helps:
        no_of_vols = VolunteeredHelp.objects.filter(volunteer_help=help).count()
        upcoming_helps_noOfVol_info.append((help, no_of_vols))

    context = {
        "upcoming_helps": upcoming_helps_noOfVol_info,
        "expired_helps_info": expired_helps_info,
        "user": user,
        "appuser": appuser,
    }

    # Render a template with the upcoming VolunteerHelp instances
    return render(request, "screens/patient_volunteer_helps.html", context)


# This view allows users to create a help
class CreateHelp(CreateView):
    model = VolunteerHelp
    form_class = CreateHelpForm
    template_name = "screens/create_help.html"

    def get_success_url(self):
        return reverse_lazy("patient_volunteer_helps")

    def form_valid(self, form):
        # Automatically set the creator field to the current user
        app_user = AppUser.objects.get(user=self.request.user)
        form.instance.user = app_user
        # Save the form and return the response
        return super().form_valid(form)


# This view allows users to update their registered help tasks
class UpdateHelp(UpdateView):
    model = VolunteerHelp
    form_class = UpdateHelpForm
    template_name = "screens/update_help.html"

    def get_success_url(self):
        return reverse_lazy("patient_volunteer_helps")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Add the pk value to the form kwargs
        kwargs["pk"] = self.kwargs.get("pk")
        return kwargs
    def form_valid(self, form):
        # Save the form and return the response
        return super().form_valid(form)


@login_required
def deleteHelp(request, id):
    # This view allows an authenticated user to delete a specific VolunteerHelp instance.
    # The 'id' parameter is the primary key of the VolunteerHelp to be deleted.

    # Retrieve the VolunteerHelp instance by its ID or return a 404 error if not found.
    help = get_object_or_404(VolunteerHelp, id=id)

    # Delete the retrieved VolunteerHelp instance.
    help.delete()

    # Redirect the user to the 'patient_volunteer_helps' view after deletion.
    return HttpResponseRedirect("../patient_volunteer_helps")


@login_required
def viewHelpDetail(request):
    # This view displays the details of a specific VolunteerHelp instance.
    # It retrieves the 'helpId' from the query parameters of the request URL.

    # Get the authenticated user and the corresponding AppUser instance.
    user = request.user
    appuser = get_object_or_404(AppUser, user=user)

    help_expired = False

    if request.GET.get("expired_help"):
        if request.GET.get("expired_help") == "true":
            help_expired = True

    # Retrieve 'helpId' from the query parameters. Defaults to None if not present.
    help_id = request.GET.get("helpId")

    if VolunteerHelp.objects.filter(id=help_id).exists():
        # Retrieve the VolunteerHelp instance by its ID or return a 404 error if not found.
        volunteer_help = get_object_or_404(VolunteerHelp, id=help_id)

        # Query for all VolunteeredHelp instances associated with the retrieved VolunteerHelp.
        volunteered_helps = VolunteeredHelp.objects.filter(
            volunteer_help=volunteer_help
        )

        # Count the number of VolunteeredHelp instances to display the volunteer count.
        volunteer_count = volunteered_helps.count()

        # Context dictionary to pass data to the template.
        context = {
            "user": user,
            "appuser": appuser,
            "volunteer_help": volunteer_help,
            "volunteered_helps": volunteered_helps,
            "volunteer_count": volunteer_count,
            "help_expired":help_expired
        }

        # Render the 'view_help_detail.html' template with the provided context.
        return render(request, "screens/view_help_detail.html", context)
    else:
        return HttpResponseRedirect(
            f"../all_patient_volunteer_helps/?expired_help=true"
        )


@login_required
def deleteVolunteer(request, volunteered_help_id, volunteer_help_id):
    # This view allows an authenticated user to delete a specific VolunteeredHelp instance.
    # The 'volunteered_help_id' parameter is the primary key of the VolunteeredHelp to be deleted.

    # Retrieve the VolunteeredHelp instance by its ID or return a 404 error if not found.
    volunteered_help = get_object_or_404(VolunteeredHelp, id=volunteered_help_id)

    # Delete the retrieved VolunteeredHelp instance.
    volunteered_help.delete()

    # Redirect the user back to the 'view_help_detail' view for the associated VolunteerHelp,
    return HttpResponseRedirect(
        f"../../view_help_detail/?helpId={volunteer_help_id}#volunteer_title"
    )


@login_required
def allPatientVolunteerHelps(request):
    user = request.user  # Get the authenticated user
    appuser = AppUser.objects.get(user=user)

    help_expired = False

    if request.GET.get("expired_help"):
        if request.GET.get("expired_help") == "true":
            help_expired = True

    # Get the current time
    now = timezone.now()

    # Retrieve the selected category from the request's GET parameters
    selected_category = request.GET.get("category")

    # Query all categories
    categories = ["grocery", "house_cleaning", "emotional", "others"]

    # Query VolunteerHelp based on the selected category and the current time.
    if selected_category:
        volunteer_helps = VolunteerHelp.objects.filter(
            category=selected_category, preferred_date_time__gt=now
        ).order_by("-created_at")
    else:
        volunteer_helps = VolunteerHelp.objects.filter(
            category="grocery", preferred_date_time__gt=now
        ).order_by("-created_at")

    # Add the count of volunteer for each volunteer help instances that still need volunteers (haven't reached the volunteer limit)  to the context
    upcoming_helps_with_volunteer_count = []
    for volunteer_help in volunteer_helps:
        volunteer_count = VolunteeredHelp.objects.filter(
            volunteer_help=volunteer_help
        ).count()
        if not VolunteeredHelp.objects.filter(
            volunteer_help=volunteer_help, user=appuser
        ).exists():
            if volunteer_count < volunteer_help.volunteer_limit:
                upcoming_helps_with_volunteer_count.append(
                    (volunteer_help, volunteer_count)
                )

    any_field_changed = False
    if VolunteeredHelp.objects.filter(user=appuser).exists():
        volunteered_helps = VolunteeredHelp.objects.filter(user=appuser)
        for volunteered_help in volunteered_helps:
            if volunteered_help.preferred_date_time_field_changed:
                any_field_changed = True
                break

            if volunteered_help.title_field_changed:
                any_field_changed = True
                break

            if volunteered_help.description_field_changed:
                any_field_changed = True
                break

            if volunteered_help.duration_field_changed:
                any_field_changed = True
                break

            if volunteered_help.volunteer_limit_field_changed:
                any_field_changed = True
                break

            if volunteered_help.location_field_changed:
                any_field_changed = True
                break

    context = {
        "user": user,
        "appuser": appuser,
        "categories": categories,
        "selected_category": selected_category,
        "upcoming_helps": upcoming_helps_with_volunteer_count,
        "any_field_changed": any_field_changed,
        "help_expired": help_expired,
    }

    return render(request, "screens/all_patient_volunteer_helps.html", context)


@login_required  # Ensure only authenticated users can access this view
def volunteerCommits(request):
    user = request.user  # Get the authenticated user
    appuser = AppUser.objects.get(
        user=user
    )  # Retrieve the corresponding AppUser object for the authenticated user

    help_expired = False

    if request.GET.get("expired_help"):
        if request.GET.get("expired_help") == "true":
            help_expired = True

    # Fetch all VolunteeredHelp instances associated with the current AppUser
    volunteered_helps = VolunteeredHelp.objects.filter(user=appuser)

    # Prepare a list to hold information about each commitment
    commits_noOfVol_info_anyFieldChanged_info = []
    for volunteered_help in volunteered_helps:
        any_field_changed = False  # Initialize a flag to track if any field has changed

        # Count the number of volunteers for the associated VolunteerHelp instance
        no_of_vols = VolunteeredHelp.objects.filter(
            volunteer_help=volunteered_help.volunteer_help
        ).count()

        # Check if any of the fields indicating a change have been set to True
        if volunteered_help.preferred_date_time_field_changed:
            any_field_changed = True
        elif volunteered_help.title_field_changed:
            any_field_changed = True
        elif volunteered_help.description_field_changed:
            any_field_changed = True
        elif volunteered_help.duration_field_changed:
            any_field_changed = True
        elif volunteered_help.volunteer_limit_field_changed:
            any_field_changed = True
        elif volunteered_help.location_field_changed:
            any_field_changed = True

        # Append a tuple containing VolunteerHelp instance, number of volunteers, and change flag to the list
        commits_noOfVol_info_anyFieldChanged_info.append(
            (volunteered_help.volunteer_help, no_of_vols, any_field_changed)
        )

    # Prepare the context with the list of commitments and user information
    context = {
        "commits": commits_noOfVol_info_anyFieldChanged_info,
        "user": user,
        "appuser": appuser,
        "help_expired": help_expired,
    }

    # Render the volunteer_commits.html template with the provided context
    return render(request, "screens/volunteer_commits.html", context)


@login_required
def viewCommitDetail(request):
    # This view displays the details of a specific VolunteerHelp instance.
    # It retrieves the 'helpId' from the query parameters of the request URL.

    # Get the authenticated user and the corresponding AppUser instance.
    user = request.user
    appuser = get_object_or_404(AppUser, user=user)

    # Retrieve 'helpId' from the query parameters. Defaults to None if not present.
    help_id = request.GET.get("helpId")
    if VolunteerHelp.objects.filter(id=help_id).exists():
        # Retrieve the VolunteerHelp instance by its ID or return a 404 error if not found.
        volunteer_help = get_object_or_404(VolunteerHelp, id=help_id)

        # Query for all VolunteeredHelp instances associated with the retrieved VolunteerHelp.
        volunteered_helps = VolunteeredHelp.objects.filter(
            volunteer_help=volunteer_help
        )

        # Count the number of VolunteeredHelp instances to display the volunteer count.
        volunteer_count = volunteered_helps.count()

        # Query the VolunteeredHelp instance associated with the retrieved VolunteerHelp and the current volunteer
        all_field_changes = []
        if VolunteeredHelp.objects.filter(
            volunteer_help=volunteer_help, user=appuser
        ).exists():
            volunteered_help = VolunteeredHelp.objects.get(
                volunteer_help=volunteer_help, user=appuser
            )

            for field in volunteered_help._meta.get_fields():
                # Exclude certain fields
                if field.name not in ["volunteer_help", "user", "created_at", "id"]:
                    # Use getattr to get the field value from the instance
                    field_value = getattr(volunteered_help, field.name)

                    # Assuming the fields are BooleanFields, check if True
                    if (
                        field_value is True
                    ):  # This checks if the field indicates a change
                        # Remove '_changed' from the field name before appending
                        clean_field_name = field.name.rsplit("_field_changed", 1)[
                            0
                        ]  # This removes '_changed' from the end
                        if clean_field_name == "preferred_date_time":
                            all_field_changes.append(
                                "Event date&time has been changed."
                            )

                        elif clean_field_name == "title":
                            all_field_changes.append("Title has been changed.")

                        elif clean_field_name == "description":
                            all_field_changes.append("Description has been changed.")

                        elif clean_field_name == "duration":
                            all_field_changes.append("Event duration has been changed.")

                        elif clean_field_name == "volunteer_limit":
                            all_field_changes.append(
                                "Required no. of volunteers has been changed."
                            )

                        elif clean_field_name == "location":
                            all_field_changes.append(
                                "Location has been changed."
                            )

                        # Set the field value to False and save the change
                        setattr(volunteered_help, field.name, False)
                        volunteered_help.save(
                            update_fields=[field.name]
                        )  # Save only the changed field

        # Context dictionary to pass data to the template.
        context = {
            "user": user,
            "appuser": appuser,
            "volunteer_help": volunteer_help,
            "volunteered_helps": volunteered_helps,
            "volunteer_count": volunteer_count,
            "all_field_changes": all_field_changes,
        }

        # Render the 'view_help_detail.html' template with the provided context.
        return render(request, "screens/view_commit_detail.html", context)
    else:
        return HttpResponseRedirect(f"../volunteer_commits/?expired_help=true")


@login_required
def unCommit(request, volunteer_help_id):
    # This view allows an authenticated user to delete a specific VolunteeredHelp instance.
    # The 'volunteer_id' parameter is the primary key of the VolunteerHelp

    appuser = AppUser.objects.get(user=request.user)
    if VolunteerHelp.objects.filter(id=volunteer_help_id).exists():
        volunteer_help = VolunteerHelp.objects.get(id=volunteer_help_id)

        # Retrieve the VolunteeredHelp instance by its  or return a 404 error if not found.
        volunteered_help = get_object_or_404(
            VolunteeredHelp, volunteer_help=volunteer_help, user=appuser
        )

        # Delete the retrieved VolunteeredHelp instance.
        volunteered_help.delete()

        # Redirect the user back to the 'volunteer_commits' view for the associated volunteer,
        return HttpResponseRedirect(f"../volunteer_commits")
    else:
        return HttpResponseRedirect(f"../volunteer_commits/?expired_help=true")


# The login_required decorator ensures that only authenticated users can access this view


def diseaseOverview(request):
    # Get the authenticated user and the corresponding AppUser instance.
    user = request.user
    appuser = get_object_or_404(AppUser, user=user)

    # Try to get the 'contentId' parameter from the URL query string
    content_id = request.GET.get("contentId")

    content = None  # Initialize content variable

    if content_id:
        # If 'contentId' is provided, try to retrieve the corresponding DiseaseOverview object
        try:
            content = DiseaseOverview.objects.get(id=content_id)
        except DiseaseOverview.DoesNotExist:
            content = None
    else:
        # If no 'contentId' is provided, get the first DiseaseOverview object from the database
        content = DiseaseOverview.objects.first()

    # Render the 'disease_overview.html' template, passing the 'content' context variable
    return render(
        request,
        "screens/disease_overview.html",
        {"content": content, "appuser": appuser},
    )


def diseaseOverviewList(request):
    # Get the authenticated user and the corresponding AppUser instance.
    user = request.user
    appuser = get_object_or_404(AppUser, user=user)

    search_query = request.GET.get("q", "")
    content_list = None

    if search_query:
        # Filter DiseaseOverview objects by content containing the search query
        try:
            content_list = DiseaseOverview.objects.filter(
                content__icontains=search_query
            )
        except DiseaseOverview.DoesNotExist:
            content_list = None

    return render(
        request,
        "screens/disease_overview.html",
        {"content_list": content_list, "appuser": appuser, "query": search_query},
    )


# The login_required decorator ensures that only authenticated users can access this view


def latestResearch(request):
    # Get the authenticated user and the corresponding AppUser instance.
    user = request.user
    appuser = get_object_or_404(AppUser, user=user)

    # Try to get the 'contentId' parameter from the URL query string
    content_id = request.GET.get("contentId")

    content = None  # Initialize content variable

    if content_id:
        # If 'contentId' is provided, try to retrieve the corresponding ResearchUpdate object
        try:
            content = ResearchUpdate.objects.get(id=content_id)
        except ResearchUpdate.DoesNotExist:
            content = None
    else:
        # If no 'contentId' is provided, get the first ResearchUpdate object from the database
        content = ResearchUpdate.objects.first()

    # Render the 'latest_research.html' template, passing the 'content' context variable
    return render(
        request,
        "screens/latest_research.html",
        {"content": content, "appuser": appuser},
    )


def latestResearchList(request):
    # Get the authenticated user and the corresponding AppUser instance.
    user = request.user
    appuser = get_object_or_404(AppUser, user=user)

    search_query = request.GET.get("q", "")
    content_list = None

    if search_query:
        # Filter ResearchUpdate objects by content containing the search query
        try:
            content_list = ResearchUpdate.objects.filter(
                summary__icontains=search_query
            )
        except ResearchUpdate.DoesNotExist:
            content_list = None

    return render(
        request,
        "screens/latest_research.html",
        {"content_list": content_list, "appuser": appuser, "query": search_query},
    )


# The login_required decorator ensures that only authenticated users can access this view


def patientStory(request):
    # Get the authenticated user and the corresponding AppUser instance.
    user = request.user
    appuser = get_object_or_404(AppUser, user=user)
    # Try to get the 'contentId' parameter from the URL query string
    content_id = request.GET.get("contentId")

    content = None  # Initialize content variable

    if content_id:
        # If 'contentId' is provided, try to retrieve the corresponding PatientStory object
        try:
            content = PatientStory.objects.get(id=content_id)
        except PatientStory.DoesNotExist:
            content = None
    else:
        # If no 'contentId' is provided, get the first PatientStory object from the database
        content = PatientStory.objects.first()

    # Render the 'patient_story.html' template, passing the 'content' context variable
    return render(
        request, "screens/patient_story.html", {"content": content, "appuser": appuser}
    )


def patientStoryList(request):
    # Get the authenticated user and the corresponding AppUser instance.
    user = request.user
    appuser = get_object_or_404(AppUser, user=user)

    search_query = request.GET.get("q", "")
    content_list = None

    if search_query:
        # Filter PatientStory objects by content containing the search query
        try:
            content_list = PatientStory.objects.filter(story__icontains=search_query)
        except PatientStory.DoesNotExist:
            content_list = None

    return render(
        request,
        "screens/patient_story.html",
        {"content_list": content_list, "appuser": appuser, "query": search_query},
    )
