from django.urls import path
from .views import GetAllActivitiesView,GetHotActivitiesView,LikeActivitiesView,UploadActivityFilesView,\
    CreateActivityView,GetAllPassagesView,GetHotPassagesView,LikePassagesView,UploadPassageCoverView\
    ,CreatePassageView,GetPassageInfoView,SearchPassageView,SearchActivityView

urlpatterns = [
    path('all_activity-get/',GetAllActivitiesView.as_view()),
    path('hot_activity-get/', GetHotActivitiesView.as_view()),
    path('activity-like/', LikeActivitiesView.as_view()),
    path('activity-upload/',UploadActivityFilesView.as_view()),
    path('activity-create/',CreateActivityView.as_view()),
    path('all_passage-get/',GetAllPassagesView.as_view()),
    path('hot_passage-get/',GetHotPassagesView.as_view()),
    path('passage-like/',LikePassagesView.as_view()),
    path('passage-upload/',UploadPassageCoverView.as_view()),
    path('passage-create/',CreatePassageView.as_view()),
    path('passage_into-get/',GetPassageInfoView.as_view()),
    path('passage-search/',SearchPassageView.as_view()),
    path('activity-search/',SearchActivityView.as_view()),
]
