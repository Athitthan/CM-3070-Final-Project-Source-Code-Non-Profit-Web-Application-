
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import generics
from rest_framework import mixins
from .models import *
from .serializers import *
from django.http import HttpResponseRedirect
#from .tasks import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


#---I WROTE THIS CODE---
# View to list all AppUser objects
class AppUserList(generics.ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserListSerializer
 #---END OF CODE THAT I WROTE---    



#---I WROTE THIS CODE---
# View for detailed AppUser information
class AppUserDetail(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserListSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
 #---END OF CODE THAT I WROTE---    
    

#---I WROTE THIS CODE---
# View to list all Gallery objects
class GalleryList(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GalleryListSerializer
 #---END OF CODE THAT I WROTE---    

#---I WROTE THIS CODE---
# View for detailed Gallery information
class GalleryDetail(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    
    
    
    def create(self, request, *args, **kwargs):
        response = super(GalleryDetail, self).create(request, *args,**kwargs)
        return HttpResponseRedirect(redirect_to='../../home')
        
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
 #---END OF CODE THAT I WROTE---




# View for managing Followings
class FollowingsView(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    
    queryset = Followings.objects.all()
    serializer_class = FollowingsSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    




#---I WROTE THIS CODE---    
# View to check if a specific relationship row exists
class CheckRowExists(APIView):
    def get(self, request):
        # Get the data to check (you can pass this in the query parameters)
        current_username = request.GET.get('current_username')
        contact_username = request.GET.get('contact_username')
        current_user=AppUser.objects.get(user__username=current_username)
        contact_user=AppUser.objects.get(user__username=contact_username)



        # Perform the database check
        exists = Followings.objects.filter(current_user=current_user,following=contact_user).exists()

        # Serialize the response
        serializer = RowExistsSerializer({'exists': exists})

        return Response(serializer.data, status=status.HTTP_200_OK)
 #---END OF CODE THAT I WROTE---    


#---I WROTE THIS CODE---
# View to list all Friend relationships
class FriendList(generics.ListAPIView):
    queryset = Followings.objects.all()
    serializer_class = FriendListSerializer
 #---END OF CODE THAT I WROTE---    

#---I WROTE THIS CODE---
# View to update likes on a Gallery post
class UpdateLikes(APIView):
    def put(self, request, id):
        try:
            post = Gallery.objects.get(id=id)
        except Gallery.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateLikesSerializer(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 #---END OF CODE THAT I WROTE---    

#---I WROTE THIS CODE---
# View to list all Status objects
class StatusList(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusListSerializer
 #---END OF CODE THAT I WROTE---

#---I WROTE THIS CODE---
# View to get all posts by a specific user
class UserPostList(APIView):
    def get(self, request, id):
        try:
            posts = Gallery.objects.filter(appuser__id=id)
        except Gallery.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GallerySerializer(instance=posts,many=True)
        return Response(serializer.data)
#---END OF CODE THAT I WROTE---    

#---I WROTE THIS CODE---        
# View to get all friends of a specific user
class UserFriendList(APIView):
    def get(self, request, id):
        try:
            posts = Followings.objects.filter(current_user__id=id)
        except Followings.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FriendListSerializer(instance=posts,many=True)
        return Response(serializer.data)  
 #---END OF CODE THAT I WROTE---          

#---I WROTE THIS CODE---
# View to get the status of a specific user
class UserStatus(APIView):
    def get(self, request, id):
        try:
            post = Status.objects.get(appuser__id=id)
        except Status.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StatusListSerializer(instance=post)
        return Response(serializer.data)        
    
    #---END OF CODE THAT I WROTE---