from django.urls import path
from . import views

urlpatterns = [
    path('', views.BandList.as_view()),
    path('bands/', views.BandList.as_view()),
    path('songs/', views.SongList.as_view()),
    path('albums/', views.AlbumList.as_view()),
    path('albums/reviews/', views.AlbumReviewList.as_view()),
    path('albums/reviews/comments/', views.AlbumReviewCommentList.as_view()),
    path('albums/reviews/likes/', views.AlbumReviewCommentList.as_view()),
]