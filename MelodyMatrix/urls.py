from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('album_list/', views.AlbumListView.as_view(), name='album_list'),
        path('album_detail/<int:pk>', views.AlbumDetailView.as_view(), name='album_detail'),
        path('artists_list/', views.artist_list, name='artist_list'),
        path('artist_detail/<int:pk>', views.ArtistDetailView.as_view(), name='artist_detail'),


]
