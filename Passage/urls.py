from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PassageViewSet, HotPassagesView, MyPassagesViewSet, LikedPassagesViewSet, UploadPassageCover, \
    SearchPassagesView

router = DefaultRouter()
router.register('info', PassageViewSet, basename='')
router.register('MyPassages', MyPassagesViewSet, basename='')
router.register('LikedPassages', LikedPassagesViewSet, basename='')
urlpatterns = [
    path('', include(router.urls)),
    path('HotPassages/', HotPassagesView.as_view()),
    path('UploadPassageCover/<filename>/<title>/', UploadPassageCover.as_view()),
    path('SearchPassages/', SearchPassagesView.as_view())
]
