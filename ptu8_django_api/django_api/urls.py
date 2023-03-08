from django.urls import path
from . import views

urlpatterns = [
    path('', views.BandList.as_view()),
    path('bands/<int:pk>/', views.BandDetail.as_view()),
    path('bands/<int:band_id>/albums/', views.AlbumList.as_view()),
    path('bands/<int:band_id>/albums/<int:pk>/', views.AlbumDetail.as_view()),
    
    path('albums/<int:pk>/', views.AlbumDetail.as_view()),
    
    path('albums/<int:album_id>/songs/', views.SongList.as_view()),
    path('albums/<int:album_id>/songs/<int:pk>/', views.SongDetail.as_view()),
    
    path('albums/<int:album_id>/reviews/', views.AlbumReviewList.as_view()),
    path('albums/<int:album_id>/reviews/<int:pk>/', views.AlbumReviewDetail.as_view()),

    path('songs/<int:pk>/', views.SongDetail.as_view()),
    
    path('reviews/<int:pk>/', views.AlbumReviewDetail.as_view()),
    path('reviews/<int:review_id>/comments/', views.AlbumReviewCommentList.as_view()),
    path('reviews/<int:review_id>/likes/', views.AlbumReviewLikeList.as_view()),
    
    path('comments/<int:pk>/', views.AlbumReviewCommentDetail.as_view()),

    path('signup/', views.UserCreate.as_view()),
]