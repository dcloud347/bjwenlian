from django.urls import path
from .views import UserRegisterView, GetSchoolsView, GetClubsView, UserLoginView,GetUserAvatarView,UserLogoutView,\
    GetClubAvatarView,GetUserClubsView,GetUserLikedActivitiesView,GetUserLikedPassagesView,GetUserLoginInfoView,\
    GetMyClubsView,JoinClubsView,GetUserInfoView,GetClubInfoView,GetOtherUserInfoView,GetOtherUserAvatarView,\
    GetMyPassagesView,GetOtherUserPassagesView

urlpatterns = [
    path('user-register/', UserRegisterView.as_view()),
    path('schools-get/', GetSchoolsView.as_view()),
    path('clubs-get/', GetClubsView.as_view()),
    path('my_clubs-get/',GetMyClubsView.as_view()),
    path('my_passages-get/',GetMyPassagesView.as_view()),
    path('clubs-avatar/',GetClubAvatarView.as_view()),
    path('user-login/', UserLoginView.as_view()),
    path('user-avatar/',GetUserAvatarView.as_view()),
    path('user-logout/',UserLogoutView.as_view()),
    path('user_clubs-get/',GetUserClubsView.as_view()),
    path('liked_activities-get/',GetUserLikedActivitiesView.as_view()),
    path('liked_passages-get/',GetUserLikedPassagesView.as_view()),
    path('user-login-get/',GetUserLoginInfoView.as_view()),
    path('club-join/',JoinClubsView.as_view()),
    path('user_info-get/',GetUserInfoView.as_view()),
    path('club_info-get/',GetClubInfoView.as_view()),
    path('other_user_info-get/',GetOtherUserInfoView.as_view()),
    path('other_user_avatar-get/',GetOtherUserAvatarView.as_view()),
    path('other_user_passages-get/',GetOtherUserPassagesView.as_view())
]
