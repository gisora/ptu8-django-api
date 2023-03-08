from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.

User = get_user_model()

class Band(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='django_api/images', blank=True, null=True)
    def __str__(self) -> str:
        return self.name


class Album(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="albums")
    name = models.CharField(max_length=1000)
    cover = models.ImageField(upload_to='django_api/covers', blank=True, null=True)
    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=1000)
    duration = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")

    def __str__(self) -> str:
        return self.name


class AlbumReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="album_reviews")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="reviews")
    content = models.CharField(max_length=1000)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    def __str__(self) -> str:
        return f"{self.album.name} - {self.user.get_username()}"


class AlbumReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="album_review_comments")
    album_review = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=1000)


class AlbumReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="album_review_like")
    album_review = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name="likes")