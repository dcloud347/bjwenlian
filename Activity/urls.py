from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet,HotActivityView,LikedActivitiesViewSet,ActivityFileUploadView,DownloadAttachment,\
    SearchActivitiesView,ParticipationViewSet

router = DefaultRouter()
router.register('info', ActivityViewSet, basename='')
router.register('LikedActivities', LikedActivitiesViewSet, basename='')
router.register('Participation', ParticipationViewSet, basename='')
urlpatterns = [
    path('',include(router.urls)),
    path('HotActivities/',HotActivityView.as_view()),
    path('UploadAttachments/<title>/<filename>/',ActivityFileUploadView.as_view()),
    path('DownloadAttachments/',DownloadAttachment.as_view()),
    path('SearchActivities/',SearchActivitiesView.as_view())
]