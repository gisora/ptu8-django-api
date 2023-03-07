from rest_framework import serializers
from . import models

class BandSerializer(serializers.ModelSerializer):
    album_count = serializers.SerializerMethodField()

    def get_album_count(self, obj):
        return models.Album.objects.filter(band=obj).count()
    
    class Meta:
        model = models.Band
        fields = ('id', 'name', 'album_count', 'image')


class AlbumSerializer(serializers.ModelSerializer):
    band_name = serializers.ReadOnlyField(source='band.name')
    song_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    def get_song_count(self, obj):
        return models.Song.objects.filter(album=obj).count()
    
    def get_review_count(self, obj):
        return models.AlbumReview.objects.filter(album=obj).count()

    class Meta:
        model = models.Album
        fields = ('id', 'name', 'band_name', 'cover', 'band_id', 'song_count', 'review_count')


class SongSerializer(serializers.ModelSerializer):
    band_name = serializers.ReadOnlyField(source='band.name')
    album_name = serializers.ReadOnlyField(source='album.name')
    
    class Meta:
        model = models.Song
        fields = ('id', 'name', 'band_name', 'album_name', 'album_id', 'duration')


class AlbumReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    album_name = serializers.ReadOnlyField(source='album.name')
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return models.AlbumReviewComment.objects.filter(album_review=obj).count()
    
    def get_like_count(self, obj):
        return models.AlbumReviewLike.objects.filter(album_review=obj).count()

    class Meta:
        model = models.AlbumReview
        fields = ('id', 'user', 'user_id', 'album_name', 'album_id', 'content', 'score', 'comment_count', 'like_count')


class AlbumReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = models.AlbumReviewComment
        fields = ('id', 'user', 'user_id', 'album_review_id', 'content')


class AlbumReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlbumReviewLike
        fields = ('id', )