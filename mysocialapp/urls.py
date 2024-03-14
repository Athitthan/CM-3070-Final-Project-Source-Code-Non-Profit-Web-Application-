from django.urls import  path,include
from . import views
from . import api
from django.contrib.auth.decorators import login_required

#---I WROTE THIS CODE---
urlpatterns = [
path('',views.user_login,name='login'),
path('about_us/',views.aboutUs,name='about_us'),

path('userDetailsApi/<int:id>',views.userDetailsApi,name='userDetailsApi'),
path('register/',views.register,name='register'),
path('logout/',login_required(login_url="../")(views.user_logout),name='logout'),
path('profile/',login_required(login_url="../")(views.profile),name='profile'),
path('forum/',login_required(login_url="../")(views.forum),name='forum'),
path('patient_volunteer_helps/',login_required(login_url="../")(views.patient_volunteer_helps),name='patient_volunteer_helps'),
path('all_patient_volunteer_helps/',login_required(login_url="../")(views.allPatientVolunteerHelps),name='all_patient_volunteer_helps'),
path('volunteer_commits/',login_required(login_url="../")(views.volunteerCommits),name='volunteer_commits'),
path('disease_overview/',login_required(login_url="../")(views.diseaseOverview),name='disease_overview'),
path('disease_overview_list/',login_required(login_url="../")(views.diseaseOverviewList),name='disease_overview_list'),
path('latest_research/',login_required(login_url="../")(views.latestResearch),name='latest_reserach'),
path('latest_research_list/',login_required(login_url="../")(views.latestResearchList),name='latest_research_list'),
path('patient_story/',login_required(login_url="../")(views.patientStory),name='patient_story'),
path('patient_story_list/',login_required(login_url="../")(views.patientStoryList),name='patient_story_list'),








path('user_forum_posts/',login_required(login_url="../")(views.userForumPosts),name='user_forum_posts'),
path('forum_post_content/',login_required(login_url="../")(views.forumPostContent),name='forum_post_content'),
path('view_help_detail/',login_required(login_url="../")(views.viewHelpDetail),name='view_help_detail'),
path('view_commit_detail/',login_required(login_url="../")(views.viewCommitDetail),name='view_commit_detail'),


path('user_profile/<str:contact_username>',login_required(login_url="../")(views.userProfile),name='user_home'),
path('follow/',login_required(login_url="../")(views.follow),name='follow'),
path('request/',login_required(login_url="../")(views.request),name='request'),
path('chatRoom/<str:contact_username>',login_required(login_url="../")(views.chatRoom),name='chatRoom'),


path('check_unread_message/',login_required(login_url="../")(views.check_unread_messages),name='check_unread_message'),
path('update_user_profile/<int:pk>',login_required(login_url="../")(views.UserProfileUpdate.as_view()),name='updateProfile'),
path('update_forum_post/<int:pk>',login_required(login_url="../")(views.UpdateForumPost.as_view()),name='updateForumPost'),
path('update_help/<int:pk>',login_required(login_url="../")(views.UpdateHelp.as_view()),name='update_help'),
path('create_forum_post/<int:pk>',login_required(login_url="../")(views.CreateForumPost.as_view()),name='createForumPost'),
path('create_help/<int:pk>',login_required(login_url="../")(views.CreateHelp.as_view()),name='create_help'),
path('api/users',api.AppUserList.as_view(),name='users_api'),
path('api/appUserDetail/<int:pk>',login_required(login_url="../")(api.AppUserDetail.as_view()),name='appUserDetail'),
path('api/followings/create/', api.FollowingsView.as_view(), name='followings-create'),
path('api/checkRowExists/', api.CheckRowExists.as_view(), name='checkRowExists'),
path('api/checkRequestRowExists/', api.CheckRequestRowExists.as_view(), name='checkRequestRowExists'),
path('api/friendList/', api.FriendList.as_view(), name='friendList'),
path('api/requestList/', api.RequestList.as_view(), name='requestList'),
path('api/search_disease_overview/', api.SearchDiseaseOverview.as_view(), name='search_disease_overview'),
path('api/search_latest_research/', api.SearchLatestResearch.as_view(), name='search_latest_research'),
path('api/search_patient_story/', api.SearchPatientStory.as_view(), name='search_patient_story'),



path('api/galleryList/', api.GalleryList.as_view(), name='galleryList'),
path('api/galleryDetail/', api.GalleryDetail.as_view(), name='galleryDetail'),
path('api/forumCommentDetail/', api.ForumCommentDetail.as_view(), name='forumCommentDetail'),
path('api/forumReplyDetail/', api.ForumReplyDetail.as_view(), name='forumReplyDetail'),
path('api/commit_to_volunteer_help/', api.CommitToVolunteerHelp.as_view(), name='commit_to_volunteer_help'),


path('api/updateLikes/<int:id>', api.UpdateLikes.as_view(), name='updateLikes'),
path('api/statusList', api.StatusList.as_view(), name='statusList'),

path('updateStatus/<int:id>',login_required(login_url="../")(views.updateStatus),name='updateStatus'),
path('deletePost/<int:id>', views.deletePost, name='deletePost'),
path('deleteHelp/<int:id>', views.deleteHelp, name='deleteHelp'),
path('deleteVolunteer/<int:volunteered_help_id>/<int:volunteer_help_id>', views.deleteVolunteer, name='deleteVolunteer'),
path('unCommit/<int:volunteer_help_id>', views.unCommit, name='unCommit'),



path('deleteForumPost/<int:id>', views.deleteForumPost, name='deleteForumPost'),
path('deleteForumPostComment/<int:comment_id>/<int:post_id>', views.deleteForumPostComment, name='deleteForumPostComment'),
path('deleteForumPostReply/<int:reply_id>/<int:post_id>', views.deleteForumPostReply, name='deleteForumPostReply'),

path('api/userPostList/<int:id>', api.UserPostList.as_view(), name='userPostList'),
path('api/userFriendList/<int:id>', api.UserFriendList.as_view(), name='userFriendList'),
path('api/userStatus/<int:id>', api.UserStatus.as_view(), name='userStatus'),

]
#---END OF CODE THAT I WROTE---