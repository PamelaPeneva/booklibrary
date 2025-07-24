from django import forms
from .models import Book, Comment, Rating, Subscriber

from .utils import get_year_choices


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'published', 'content', 'author', 'genres', 'pdf_file']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'published': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Content',
            }),
            'genres': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',

            })
        }

class BookEditForm(BookForm):
    pass

class BookDeleteForm(BookForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.disabled = True
            field.widget.attrs["readonly"] = True


class BookSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by title or author',
        })
    )

    date_search_query = forms.ChoiceField(
        choices=[],
        required=False,
        label="Published Year"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_search_query'].choices = get_year_choices()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        labels = {
            'content': '',
        }

        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Add a comment',
                'id': 'my-textarea'
            })
        }

class RatingForm(forms.ModelForm):
    class Meta:

        model = Rating
        fields = ['score']
        labels = {
            'score': 'Rate this book (1-5 stars)',
        }

        choices = [(i, i) for i in range(1, 6)]
        widgets = {
            'score': forms.Select(choices=choices),
        }


class EmailSubscriptionForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True,
        }),
        label=""
    )

