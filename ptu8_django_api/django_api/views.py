from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from . import models, serializers


# Create your views here.
class UserOwnedObjectRUDMixin():
    def delete(self, request, *args, **kwargs):
        obj = self.queryset.filter(pk=kwargs['pk'], user=self.request.user)
        if obj.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))

    def put(self, request, *args, **kwargs):
        obj = self.queryset.filter(pk=kwargs['pk'], user=self.request.user)
        if obj.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))


class BandList(generics.ListCreateAPIView):
    serializer_class = serializers.BandSerializer
    queryset = models.Band.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        if self.request.user.is_superuser or self.request.user.is_staff:
            serializer.save()
        else:
            raise ValidationError(_('Only staff user can add new values.'))


class BandDetail(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
    serializer_class = serializers.BandSerializer
    queryset = models.Band.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class AlbumList(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        if self.request.user.is_superuser or self.request.user.is_staff:
            serializer.save(band=models.Band.objects.get(id=self.kwargs['band_id']))
        else:
            raise ValidationError(_('Only staff user can add new values.'))
        

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(band=models.Band.objects.get(id=self.kwargs['band_id']))
        return qs


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class SongList(generics.ListCreateAPIView):
    serializer_class = serializers.SongSerializer
    queryset = models.Song.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        if self.request.user.is_superuser or self.request.user.is_staff:
            serializer.save(album=models.Album.objects.get(id=self.kwargs['album_id']))
        else:
            raise ValidationError(_('Only staff user can add new values.'))


    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(album=models.Album.objects.get(id=self.kwargs['album_id']))
        return qs


class SongDetail(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
    serializer_class = serializers.SongSerializer
    queryset = models.Song.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class AlbumReviewList(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumReviewSerializer
    queryset = models.AlbumReview.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            album=models.Album.objects.get(id=self.kwargs['album_id']),
        )
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(album=models.Album.objects.get(id=self.kwargs['album_id']))
        return qs


class AlbumReviewDetail(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
    serializer_class = serializers.AlbumReviewSerializer
    queryset = models.AlbumReview.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class AlbumReviewCommentList(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumReviewCommentSerializer
    queryset = models.AlbumReviewComment.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            album_review=models.AlbumReview.objects.get(id=self.kwargs['review_id']),
        )

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(album_review=models.AlbumReview.objects.get(id=self.kwargs['review_id']))
        return qs


class AlbumReviewCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AlbumReviewCommentSerializer
    queryset = models.AlbumReviewComment.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def delete(self, request, *args, **kwargs):
        obj = self.queryset.filter(pk=kwargs['pk'], user=self.request.user)
        if obj.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))

    def put(self, request, *args, **kwargs):
        obj = self.queryset.filter(pk=kwargs['pk'], user=self.request.user)
        if obj.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))


class AlbumReviewLikeList(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.AlbumReviewLikeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return models.AlbumReviewLike.objects.filter(
            user=self.request.user,
            album_review=models.AlbumReview.objects.get(id=self.kwargs['review_id']),
        )

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_('You already like this.'))
        else:
            serializer.save(
                user=self.request.user,
                album_review=models.AlbumReview.objects.get(id=self.kwargs['review_id']),
            )

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_('You cannot unlike what you don\'t like.'))