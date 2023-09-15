from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import AppUser, Status, Gallery, Followings
from .model_factories import AppUserFactory, StatusFactory, GalleryFactory, FollowingsFactory

#---I WROTE THIS CODE---

class AppUserListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test AppUser instances using factories
        self.app_user1 = AppUserFactory()
        self.app_user2 = AppUserFactory()

    def test_get_app_users(self):
        # Test the AppUserList view
        response = self.client.get('/api/users')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if the response contains the expected number of objects


class StatusListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test Status instances using factories
        self.status1 = StatusFactory()
        self.status2 = StatusFactory()

    def test_get_statuses(self):
        # Test the StatusList view
        response = self.client.get('/api/statusList')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if the response contains the expected number of objects


class GalleryListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test Gallery instances using factories
        self.gallery1 = GalleryFactory()
        self.gallery2 = GalleryFactory()

    def test_get_galleries(self):
        # Test the GalleryList view
        response = self.client.get('/api/galleryList')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if the response contains the expected number of objects


class FollowingsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test Followings instances using factories
        self.followings1 = FollowingsFactory()
        self.followings2 = FollowingsFactory()

    def test_get_followings(self):
        # Test the FollowingsView view
        response = self.client.get('/api/friendList')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if the response contains the expected number of objects

#---END OF CODE THAT I WROTE---