from django.urls import  path,include
from . import views
from . import api
from django.contrib.auth.decorators import login_required

#---I WROTE THIS CODE---
urlpatterns = [
path('',views.user_login,name='login'),
path('userDetailsApi/<int:id>',views.userDetailsApi,name='userDetailsApi'),
path('register/',views.register,name='register'),
path('logout/',login_required(login_url="../")(views.user_logout),name='logout'),
path('home/',login_required(login_url="../")(views.home),name='home'),
path('user_home/<str:contact_username>',login_required(login_url="../")(views.userHome),name='user_home'),
path('follow/',login_required(login_url="../")(views.follow),name='follow'),
path('chatRoom/<str:contact_username>',login_required(login_url="../")(views.chatRoom),name='chatRoom'),

path('update_user_profile/<int:pk>',login_required(login_url="../")(views.UserProfileUpdate.as_view()),name='updateProfile'),

path('api/users',api.AppUserList.as_view(),name='users_api'),
path('api/appUserDetail/<int:pk>',login_required(login_url="../")(api.AppUserDetail.as_view()),name='appUserDetail'),

path('api/followings/create/', api.FollowingsView.as_view(), name='followings-create'),

path('api/checkRowExists/', api.CheckRowExists.as_view(), name='checkRowExists'),
path('api/friendList/', api.FriendList.as_view(), name='friendList'),
path('api/galleryList/', api.GalleryList.as_view(), name='galleryList'),
path('api/galleryDetail/', api.GalleryDetail.as_view(), name='galleryDetail'),
path('api/updateLikes/<int:id>', api.UpdateLikes.as_view(), name='updateLikes'),
path('api/statusList', api.StatusList.as_view(), name='statusList'),

path('updateStatus/<int:id>',login_required(login_url="../")(views.updateStatus),name='updateStatus'),
path('deletePost/<int:id>', views.deletePost, name='deletePost'),
path('api/userPostList/<int:id>', api.UserPostList.as_view(), name='userPostList'),
path('api/userFriendList/<int:id>', api.UserFriendList.as_view(), name='userFriendList'),
path('api/userStatus/<int:id>', api.UserStatus.as_view(), name='userStatus'),

]
#---END OF CODE THAT I WROTE---