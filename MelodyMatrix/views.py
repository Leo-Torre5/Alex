from .models import Album, Artist, AlbumInstance, Genre
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse



def index(request):
    """View function for home page of the site."""
    num_albums = Album.objects.all().count()
    num_instances = AlbumInstance.objects.all().count()
    num_instances_available = AlbumInstance.objects.filter(status__exact='a').count()
    num_artists = Artist.objects.count() # Add this line to get the count of artists.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_albums': num_albums,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_artists': num_artists,# Include num_artists in the context
        'num_visits': num_visits,}
    return render(request, 'index.html', context=context)


def artist_list(request):
    artists = Artist.objects.all()  # Replace with your actual query
    return render(request, 'MelodyMatrix/artist_list.html', {'artist_list': artists})


def artist_detail(request, artist_id):
    artist = Artist.objects.get(pk=artist_id)
    return render(request, 'MelodyMatrix/artist_detail.html', {'artist': artist})

class AlbumListView(LoginRequiredMixin, generic.ListView):
    model = Album

class AlbumDetailView(LoginRequiredMixin, generic.DetailView):
    model = Album


class ArtistListView(LoginRequiredMixin, generic.ListView):
    model = Artist
    # This is where
    fields = ['artist_image']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('artist_list'))


class ArtistDetailView(generic.DetailView):
    model = Artist
    fields = ['artist_image']
#above added the fields artist_image and album_image with the HTTP for the site.
    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        return HttpResponseRedirect(reverse('artist_list'))


def search(request):
    search_query = request.GET.get('query', '')
    if search_query:
        # Perform a case-insensitive search on the name field of artists,
        # title field of albums, and name field of genres
        artist_results = Artist.objects.filter(name__icontains=search_query)
        album_results = Album.objects.filter(title__icontains=search_query)
        genre_results = Genre.objects.filter(name__icontains=search_query)
        return render(request, 'search_results.html', {'search_query': search_query, 'artist_results': artist_results, 'album_results': album_results, 'genre_results': genre_results})
    return render(request, 'search_results.html', {'search_query': search_query})

