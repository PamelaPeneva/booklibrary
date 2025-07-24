from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    fav_books = models.ManyToManyField('books.Book', blank=True, related_name='favorited_by')



