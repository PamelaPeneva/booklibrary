from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
UserModel = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default='Anonymous')
    published = models.DateField(null=True, blank=True,
    default='2000-12-12')  # YYYY-MM-DD
    content = models.TextField(
        blank=True,
        null=True,
    )

    genres = models.ManyToManyField(Genre, related_name='books')

    pdf_file = models.FileField(upload_to='media_files/pdfs/', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(
        validators=[MinLengthValidator(1),],
    )
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name='comments')

class Rating(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')  # Each user can rate a book once

    def __str__(self):
        return f"{self.user} rated {self.book} - {self.score}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

