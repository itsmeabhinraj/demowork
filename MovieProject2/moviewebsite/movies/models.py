from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    # movie_id = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250)
    desc = models.TextField(max_length=250)
    year = models.DateField()
    img = models.ImageField(upload_to='gallery')
    actors = models.CharField(max_length=250, default="unknown")
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    trailer_link = models.URLField(max_length=250, default="unknown")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# there is no model wishlist
class Wishlist(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"
