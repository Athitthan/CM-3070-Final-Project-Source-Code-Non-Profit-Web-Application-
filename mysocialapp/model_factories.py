import factory
from django.contrib.auth.models import User
from .models import *

# ---I WROTE THIS CODE---


# Factory for User model
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")


# Factory for AppUser model
class AppUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AppUser

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    email = factory.Faker("email")
    # Add more fields as needed


# Factory for Status model
class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    status = factory.Faker("text")
    appuser = factory.SubFactory(AppUserFactory)


# Factory for Gallery model
class GalleryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gallery

    post_image = factory.django.ImageField(filename="example.jpg")
    description = factory.Faker("text")
    likes = factory.Faker("random_int")
    appuser = factory.SubFactory(AppUserFactory)


# Factory for Followings model
class FollowingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Followings

    current_user = factory.SubFactory(AppUserFactory)
    following = factory.SubFactory(AppUserFactory)


# Factory for ChatMessage model
class ChatMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatMessage

    room_name = factory.Faker("word")
    sender = factory.Faker("user_name")
    message = factory.Faker("text")


# ---END OF CODE THAT I WROTE---


class ForumPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ForumPost

    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    creator = factory.SubFactory(AppUserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(ForumPostFactory)
    content = factory.Faker("text")
    creator = factory.SubFactory(AppUserFactory)


class ReplyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reply

    comment = factory.SubFactory(CommentFactory)
    content = factory.Faker("text")
    creator = factory.SubFactory(AppUserFactory)


class VolunteerHelpFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VolunteerHelp

    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    user = factory.SubFactory(AppUserFactory)


class DiseaseOverviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DiseaseOverview

    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")


class ResearchUpdateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResearchUpdate

    title = factory.Faker("sentence")
    summary = factory.Faker("paragraph")


class PatientStoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientStory

    title = factory.Faker("sentence")
    story = factory.Faker("paragraph")
