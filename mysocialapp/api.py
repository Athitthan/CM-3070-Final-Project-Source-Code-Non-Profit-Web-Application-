from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *
from django.http import HttpResponseRedirect

# from .tasks import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# ---I WROTE THIS CODE---
# View to list all AppUser objects
class AppUserList(generics.ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserListSerializer


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View for detailed AppUser information
class AppUserDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = AppUser.objects.all()
    serializer_class = AppUserListSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View to list all Gallery objects
class GalleryList(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GalleryListSerializer


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View for detailed Gallery information
class GalleryDetail(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def create(self, request, *args, **kwargs):
        response = super(GalleryDetail, self).create(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to="../../profile#status_container")

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# ---END OF CODE THAT I WROTE---


# View for managing Followings
class FollowingsView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Followings.objects.all()
    serializer_class = FollowingsSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# ---I WROTE THIS CODE---
# View to check if a specific relationship row exists
class CheckRowExists(APIView):
    def get(self, request):
        # Get the data to check (you can pass this in the query parameters)
        current_username = request.GET.get("current_username")
        contact_username = request.GET.get("contact_username")
        current_user = AppUser.objects.get(user__username=current_username)
        contact_user = AppUser.objects.get(user__username=contact_username)

        # Perform the database check
        exists = Followings.objects.filter(
            current_user=current_user, following=contact_user
        ).exists()

        # Serialize the response
        serializer = RowExistsSerializer({"exists": exists})

        return Response(serializer.data, status=status.HTTP_200_OK)


# ---END OF CODE THAT I WROTE---


# View to check if a specific relationship row exists
class CheckRequestRowExists(APIView):
    def get(self, request):
        # Get the data to check (you can pass this in the query parameters)
        requested_user_username = request.GET.get("requestedUserUsername")
        requester_username = request.GET.get("requesterUsername")
        requested_user = AppUser.objects.get(user__username=requested_user_username)
        requester = AppUser.objects.get(user__username=requester_username)

        # Perform the database check
        exists = Request.objects.filter(
            requested_user=requested_user, requester=requester
        ).exists()

        # Serialize the response
        serializer = RowExistsSerializer({"exists": exists})

        return Response(serializer.data, status=status.HTTP_200_OK)


# ---I WROTE THIS CODE---
# View to list all Friend relationships
class FriendList(generics.ListAPIView):
    queryset = Followings.objects.all()
    serializer_class = FriendListSerializer


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View to list all Friend relationships
class RequestList(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestListSerializer


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View to update likes on a Gallery post
class UpdateLikes(APIView):
    def put(self, request, id):
        try:
            post = Gallery.objects.get(id=id)
        except Gallery.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateLikesSerializer(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View to list all Status objects
class StatusList(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusListSerializer


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View to get all posts by a specific user
class UserPostList(APIView):
    def get(self, request, id):
        try:
            posts = Gallery.objects.filter(appuser__id=id)
        except Gallery.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = GallerySerializer(instance=posts, many=True)
        return Response(serializer.data)


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View to get all friends of a specific user
class UserFriendList(APIView):
    def get(self, request, id):
        try:
            posts = Followings.objects.filter(current_user__id=id)
        except Followings.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = FriendListSerializer(instance=posts, many=True)
        return Response(serializer.data)


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# View to get the status of a specific user
class UserStatus(APIView):
    def get(self, request, id):
        try:
            post = Status.objects.get(appuser__id=id)
        except Status.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = StatusListSerializer(instance=post)
        return Response(serializer.data)

    # ---END OF CODE THAT I WROTE---


class ForumCommentDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    API view to handle CRUD operations for forum comments.
    """

    queryset = Comment.objects.all()  # Queryset for all comments
    serializer_class = ForumCommentSerializer  # Serializer class for forum comments

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle the creation of a forum comment,
        then redirect to the forum post content page.
        """
        post_id = request.POST["post"]  # Extract the post ID from the request
        # Call the superclass's create method to handle actual comment creation
        response = super(ForumCommentDetail, self).create(request, *args, **kwargs)
        # Redirect to the forum post content page with the post ID
        return HttpResponseRedirect(
            redirect_to=f"../../forum_post_content/?postId={post_id}#forum_post_content_footer"
        )

    def post(self, request, *args, **kwargs):
        """
        POST method for creating a forum comment.
        """
        return self.create(request, *args, **kwargs)  # Delegate to the create method


class ForumReplyDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    API view to handle CRUD operations for forum replies.
    """

    queryset = Reply.objects.all()  # Queryset for all replies
    serializer_class = ForumReplySerializer  # Serializer class for forum replies

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle the creation of a forum reply,
        then redirect to the specific comment section in the forum post.
        """
        post_id = request.POST["post"]  # Extract the post ID from the request
        comment_id = request.POST["comment"]  # Extract the comment ID from the request
        # Call the superclass's create method to handle actual reply creation
        response = super(ForumReplyDetail, self).create(request, *args, **kwargs)
        # Redirect to the forum post content page with the post ID and anchor to the comment
        return HttpResponseRedirect(
            redirect_to=f"../../forum_post_content/?postId={post_id}#comment_container_{comment_id}"
        )

    def post(self, request, *args, **kwargs):
        """
        POST method for creating a forum reply.
        """
        return self.create(request, *args, **kwargs)  # Delegate to the create method


class CommitToVolunteerHelp(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    """
    API view to handle the creation of commitments to volunteer help.
    """

    queryset = (
        VolunteeredHelp.objects.all()
    )  # Queryset for all volunteered help commitments
    serializer_class = CommitToVolunteerHelpSerializer  # Serializer class for committing to volunteer help

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle the creation of a volunteer help commitment,
        then redirect to the volunteer commits page.
        """
        volunteer_help_id = request.POST["volunteer_help"]
        if VolunteerHelp.objects.filter(id=volunteer_help_id).exists():
            # Call the superclass's create method to handle actual commitment creation
            response = super(CommitToVolunteerHelp, self).create(
                request, *args, **kwargs
            )
            # Redirect to the volunteer commits page
            return HttpResponseRedirect(redirect_to="../../volunteer_commits")
        else:
            return HttpResponseRedirect(redirect_to="../../all_patient_volunteer_helps/?expired_help=true")

    def post(self, request, *args, **kwargs):
        """
        POST method for creating a volunteer help commitment.
        """
        return self.create(request, *args, **kwargs)  # Delegate to the create method


class SearchDiseaseOverview(APIView):
    """
    API view to search DiseaseOverview instances by titles that start with the provided query.
    """

    def get(self, request, format=None):
        """
        GET method to perform the search operation.
        """
        query = request.GET.get("q", "")  # Extract query parameter
        if query:
            # Filter DiseaseOverview instances where title starts with query
            overviews = DiseaseOverview.objects.filter(title__istartswith=query)
            # Serialize and return the filtered DiseaseOverview instances
            serializer = DiseaseOverviewSerializer(overviews, many=True)
            return Response(serializer.data)
        return Response([])  # Return an empty list if no query is provided


class SearchLatestResearch(APIView):
    """
    API view to search ResearchUpdate instances by titles that start with the provided query.
    """

    def get(self, request, format=None):
        """
        GET method to perform the search operation.
        """
        query = request.GET.get("q", "")  # Extract query parameter
        if query:
            # Filter ResearchUpdate instances where title starts with query
            overviews = ResearchUpdate.objects.filter(title__istartswith=query)
            # Serialize and return the filtered ResearchUpdate instances
            serializer = ResearchUpdateSerializer(overviews, many=True)
            return Response(serializer.data)
        return Response([])  # Return an empty list if no query is provided


class SearchPatientStory(APIView):
    """
    API view to search PatientStory instances by titles that start with the provided query.
    """

    def get(self, request, format=None):
        """
        GET method to perform the search operation.
        """
        query = request.GET.get("q", "")  # Extract query parameter
        if query:
            # Filter ResearchUpdate instances where title starts with query
            overviews = PatientStory.objects.filter(title__istartswith=query)
            # Serialize and return the filtered ResearchUpdate instances
            serializer = PatientStorySerializer(overviews, many=True)
            return Response(serializer.data)
        return Response([])  # Return an empty list if no query is provided
