# Import necessary modules and classes
from django.utils import timezone
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

# ---I WROTE THIS CODE---


# Define a form for user registration
class UserForm(forms.ModelForm):
    # Define a password field with a password input widget
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password"]


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Define a form for user profile information
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ["name","group"]

    # Define a required name field
    name = forms.CharField(required=True)


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Define a form for user login
class UserLoginForm(forms.Form):
    # Define username and password fields with appropriate widgets
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Define a form for editing user profile information
class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ["name", "email", "profile_image", "background_image", "bio"]

    # Define a required name field
    name = forms.CharField(required=True)


# ---END OF CODE THAT I WROTE---


# Define a form for creating forum post
class CreateForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ["title", "image", "content", "category"]

    # Define a required name field
    title = forms.CharField(required=True)


# Define a form for updating forum post
class UpdateForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ["title", "image", "content"]

    # Define a required name field
    title = forms.CharField(required=True)


# Define a form for creating a help
class CreateHelpForm(forms.ModelForm):
    class Meta:
        model = VolunteerHelp
        fields = [
            "title",
            "description",
            "preferred_date_time",
            "location",
            "duration",
            "category",
            "volunteer_limit",
        ]

    # Define a required name field
    title = forms.CharField(required=True)

    def clean_preferred_date_time(self):
        preferred_date = self.cleaned_data["preferred_date_time"].date()
        current_date = timezone.localtime(timezone.now()).date()

        if preferred_date <= current_date:
            raise ValidationError(
                "The preferred date must be at least a day after today's date."
            )
        return self.cleaned_data["preferred_date_time"]


# Define a form for creating a help
class UpdateHelpForm(forms.ModelForm):
    class Meta:
        model = VolunteerHelp
        fields = [
            "title",
            "description",
            "duration",
            "location",
            "volunteer_limit",
            "preferred_date_time",
        ]

    # Define a required name field
    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        # Extract the pk argument
        self.pk = kwargs.pop("pk", None)
        super().__init__(*args, **kwargs)

    def clean_preferred_date_time(self):
        preferred_date_time = self.cleaned_data["preferred_date_time"]
        current_date_time = timezone.localtime(timezone.now())

        if preferred_date_time.date() <= current_date_time.date():
            raise ValidationError(
                "The preferred date must be atleast a day apart from the current date"
            )
        volunteer_help = VolunteerHelp.objects.get(id=self.pk)
        if preferred_date_time != volunteer_help.preferred_date_time:
            volunteered_helps = VolunteeredHelp.objects.filter(volunteer_help=volunteer_help)
            for help in volunteered_helps:
                help.preferred_date_time_field_changed = True
                help.save()
        return preferred_date_time

    def clean_title(self):
        title = self.cleaned_data["title"]
        volunteer_help = VolunteerHelp.objects.get(id=self.pk)
        if title != volunteer_help.title:
            volunteered_helps = VolunteeredHelp.objects.filter(volunteer_help=volunteer_help)
            for help in volunteered_helps:
                help.title_field_changed = True
                help.save()
        return title

    def clean_location(self):
        location = self.cleaned_data["location"]
        volunteer_help = VolunteerHelp.objects.get(id=self.pk)
        if location != volunteer_help.location:
            volunteered_helps = VolunteeredHelp.objects.filter(
                volunteer_help=volunteer_help
            )
            for help in volunteered_helps:
                help.location_field_changed = True
                help.save()
        return location

    def clean_description(self):
        description = self.cleaned_data["description"]
        volunteer_help = VolunteerHelp.objects.get(id=self.pk)
        if description != volunteer_help.description:
            volunteered_helps = VolunteeredHelp.objects.filter(volunteer_help=volunteer_help)
            for help in volunteered_helps:
                help.description_field_changed = True
                help.save()
        return description

    def clean_duration(self):
        duration = self.cleaned_data["duration"]
        volunteer_help = VolunteerHelp.objects.get(id=self.pk)
        if duration != volunteer_help.duration:
            volunteered_helps = VolunteeredHelp.objects.filter(volunteer_help=volunteer_help)
            for help in volunteered_helps:
                help.duration_field_changed = True
                help.save()
        return duration

    def clean_volunteer_limit(self):
        volunteer_limit = self.cleaned_data["volunteer_limit"]
        volunteer_help = VolunteerHelp.objects.get(id=self.pk)
        volunteer_count=VolunteeredHelp.objects.filter(volunteer_help=volunteer_help).count()
        if volunteer_limit != volunteer_help.volunteer_limit:
            if volunteer_limit < volunteer_count:
                raise ValidationError("Error: Current no. of volunteers are more than the newly set limit.")
            else: 
                volunteered_helps = VolunteeredHelp.objects.filter(volunteer_help=volunteer_help)
                for help in volunteered_helps:
                    help.volunteer_limit_field_changed = True
                    help.save()
        return volunteer_limit
