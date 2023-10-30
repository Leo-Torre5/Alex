#Added all code below from Evelyn's admin.py file. -Leo
from django.contrib import admin
from .models import Album, Song, Artist, Genre, AlbumInstance


# Register your models here.
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(AlbumInstance)
admin.site.register(Song)