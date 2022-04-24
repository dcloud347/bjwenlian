from django.urls import path, include
from .views import LoginView, RegisterView,UserAvatarView,SchoolViewSet,MySimpView,UserViewSet,ClubViewSet,MyClubViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='')
router.register('schools',SchoolViewSet,basename='')
router.register('clubs',ClubViewSet,basename='')
router.register('MyClubs',MyClubViewSet,basename='')
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('',include(router.urls)),
    path('avatar/<filename>/',UserAvatarView.as_view()),
    path('MySimpView/',MySimpView.as_view())
]