from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Post.views import PostViewSet

router = DefaultRouter()
router.register('info', PostViewSet, basename='')

urlpatterns=[
    path('', include(router.urls))
]