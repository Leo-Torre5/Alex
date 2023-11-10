from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique album instances


class Genre(models.Model):
    """Model representing an album genre."""
    name = models.CharField(max_length=200, help_text='Enter an album genre (e.g.Country)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name



class Artist(models.Model):
    """Model representing an artist."""
    artist_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    artist_image = models.ImageField(upload_to='images/', null=True, blank=True)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this artist')
    summary = models.TextField(max_length=2000, help_text='Enter a brief background of the artist', null=True)

    # included an image for an artist - added it in Sprint 2
    #    artist_image = models.ImageField(upload_to='images/', null=True, blank=True)

    class Meta:
        ordering = ['artist_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular artist instance."""
        return reverse('artist_detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.artist_name}'


class Album(models.Model):
    """Model representing an Album."""
    title = models.CharField(max_length=200, null=True)
    album_image = models.ImageField(upload_to='images/', null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    # album_image = models.ImageField(upload_to='images/', null=True, blank=True)

    # Foreign Key used because album can only have one artist, but artists can have many albums
    artist = models.ForeignKey('Artist', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(max_length=2000, help_text='Enter a brief summary of the album', null=True)

    # ManyToManyField used because genre can contain many albums. Albums can cover many genres.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this album')

    duration = models.DurationField(help_text='Enter the duration of the album')
    tracks = models.IntegerField(help_text='Select the number of tracks')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this album."""
        return reverse('album_detail', args=[str(self.id)])

class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')

    def __str__(self):
        return self.title


class AlbumInstance(models.Model):
    """Model representing a specific copy of an album (that can be loaned from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular album across whole library')
    album = models.ForeignKey('Album', on_delete=models.RESTRICT, null=True)
    format = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Available'), ('o', 'On loan'), ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Album availability',
    )

    # Will implement the following in Sprint 2
    # borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # @property
    # def is_overdue(self):
    # """Determines if the album is overdue based on due date and current date."""
    # return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.album.title})'

