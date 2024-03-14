from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import *
from .model_factories import *
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

# ---I WROTE THIS CODE---


class AppUserListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test AppUser instances using factories
        self.app_user1 = AppUserFactory()
        self.app_user2 = AppUserFactory()

    def test_get_app_users(self):
        # Test the AppUserList view
        response = self.client.get("/api/users")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Check if the response contains the expected number of objects


class StatusListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test Status instances using factories
        self.status1 = StatusFactory()
        self.status2 = StatusFactory()

    def test_get_statuses(self):
        # Test the StatusList view
        response = self.client.get(
            "/api/statusList"
        )  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Check if the response contains the expected number of objects


class GalleryListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test Gallery instances using factories
        self.gallery1 = GalleryFactory()
        self.gallery2 = GalleryFactory()

    def test_get_galleries(self):
        # Test the GalleryList view
        response = self.client.get("/api/galleryList")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Check if the response contains the expected number of objects


class FollowingsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test Followings instances using factories
        self.followings1 = FollowingsFactory()
        self.followings2 = FollowingsFactory()

    def test_get_followings(self):
        # Test the FollowingsView view
        response = self.client.get(
            "/api/friendList"
        )  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 2
        )  # Check if the response contains the expected number of objects


# ---END OF CODE THAT I WROTE---


class ForumCommentDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.forum_post = ForumPostFactory()
        self.comment_data = {
            "post": self.forum_post.id,
            "content": "This is a test comment",
        }

    def test_create_forum_comment(self):
        response = self.client.post("/api/forumCommentDetail", self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class ForumReplyDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.comment = CommentFactory()
        self.reply_data = {
            "comment": self.comment.id,
            "content": "This is a test reply",
        }

    def test_create_forum_reply(self):
        response = self.client.post("/api/forumReplyDetail", self.reply_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class CommitToVolunteerHelpTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.volunteer_help = VolunteerHelpFactory()
        self.commit_data = {"volunteer_help": self.volunteer_help.id}

    def test_commit_to_volunteer_help(self):
        response = self.client.post(
            "/api/commit_to_volunteer_help", self.commit_data
        )  # Use the actual URL
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class SearchDiseaseOverviewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        DiseaseOverviewFactory(title="Cancer Overview")
        DiseaseOverviewFactory(title="Diabetes Overview")

    def test_search_disease_overview(self):
        response = self.client.get("/api/search_disease_overview/", {"q": "Cancer"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)


class SearchLatestResearchTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        ResearchUpdateFactory(title="Cancer Research 2020")
        ResearchUpdateFactory(title="Diabetes Research 2020")

    def test_search_latest_research(self):
        response = self.client.get("/api/search_latest_research/", {"q": "Cancer"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)


class SearchPatientStoryTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        PatientStoryFactory(title="John's Cancer Journey")
        PatientStoryFactory(title="Alice's Diabetes Story")

    def test_search_patient_story(self):
        response = self.client.get("/api/search_patient_story/", {"q": "Cancer"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)


# ---- views.py functions test--------


class ForumViewTest(TestCase):
    def setUp(self):
        # Create a user and an associated AppUser
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")
        self.app_user = AppUserFactory(user=self.user)

        # Create a couple of forum posts
        self.forum_post1 = ForumPostFactory(creator=self.app_user, category="treatment")
        self.forum_post2 = ForumPostFactory(creator=self.app_user, category="emotional")

    def test_forum_view(self):
        response = self.client.get(
            reverse("forum")
        )  # Use the actual name of your forum view
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.forum_post1.title)
        self.assertContains(response, self.forum_post2.title)


class CreateForumPostTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")
        self.app_user = AppUserFactory(user=self.user)

    def test_create_forum_post(self):
        post_data = {
            "title": "New Forum Post",
            "content": "Content of the new post",
            "category": "treatment",
        }
        response = self.client.post(
            reverse("create_forum_post"), post_data
        )  # Use the actual name of your create view
        self.assertEqual(
            response.status_code, 302
        )  # Assuming a redirect happens after creation


class DeleteForumPostTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")
        self.app_user = AppUserFactory(user=self.user)
        self.forum_post = ForumPostFactory(creator=self.app_user)

    def test_delete_forum_post(self):
        response = self.client.get(
            reverse("delete_forum_post", args=[self.forum_post.id])
        )  # Use the actual name of your delete view
        self.assertEqual(
            response.status_code, 302
        )  # Assuming a redirect happens after deletion


class ForumPostContentTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")
        self.app_user = AppUserFactory(user=self.user)
        self.forum_post = ForumPostFactory(creator=self.app_user)
        self.comment = CommentFactory(post=self.forum_post)
        self.reply = ReplyFactory(comment=self.comment)

    def test_forum_post_content(self):
        response = self.client.get(
            reverse("forum_post_content"), {"postId": self.forum_post.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.forum_post.title)
        self.assertContains(response, self.comment.content)
        self.assertContains(response, self.reply.content)


class UserForumPostsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")
        self.app_user = AppUserFactory(user=self.user)
        ForumPostFactory.create_batch(
            3, creator=self.app_user
        )  # Create 3 forum posts for this user

    def test_user_forum_posts(self):
        response = self.client.get(reverse("user_forum_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["forum_posts"]), 3
        )  # Expect 3 posts in the context


class DeleteForumPostCommentTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")
        self.app_user = AppUserFactory(user=self.user)
        self.post = ForumPostFactory(creator=self.app_user)
        self.comment = CommentFactory(post=self.post)

    def test_delete_comment(self):
        response = self.client.get(
            reverse("delete_forum_post_comment", args=[self.comment.id, self.post.id])
        )
        self.assertEqual(response.status_code, 302)  # Expect redirection after deletion
        self.assertFalse(
            Comment.objects.filter(id=self.comment.id).exists()
        )  # The comment should be deleted


class DeleteForumPostReplyTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")
        self.app_user = AppUserFactory(user=self.user)
        self.comment = CommentFactory()
        self.reply = ReplyFactory(comment=self.comment)

    def test_delete_reply(self):
        response = self.client.get(
            reverse(
                "delete_forum_post_reply", args=[self.reply.id, self.comment.post.id]
            )
        )
        self.assertEqual(response.status_code, 302)  # Expect redirection after deletion
        self.assertFalse(
            Reply.objects.filter(id=self.reply.id).exists()
        )  # The reply should be deleted
