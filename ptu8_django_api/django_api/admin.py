from django.contrib import admin
from . import models

# Register your models here.
class BandAdmin(admin.ModelAdmin):
    list_display = ('name', )

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('band', 'name')

class SongAdmin(admin.ModelAdmin):
    list_display = ('album', 'name', 'duration')


admin.site.register(models.Band, BandAdmin)
admin.site.register(models.Album, AlbumAdmin)
admin.site.register(models.Song, SongAdmin)
admin.site.register(models.AlbumReview)
admin.site.register(models.AlbumReviewComment)
admin.site.register(models.AlbumReviewLike)