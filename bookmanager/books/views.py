from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q
from django.http import Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, RedirectView

from accounts.mixins import StaffRequiredMixin
from .models import Book, Rating, Subscriber
from .forms import BookForm, BookEditForm, BookDeleteForm, BookSearchForm, CommentForm, RatingForm, \
    EmailSubscriptionForm
from events.models import Event

def index(request):
    upcoming_events = Event.objects.filter(start_time__gte=timezone.now()).order_by('start_time')
    now = timezone.now()

    context = {
        'events': upcoming_events,
        'time': now,
        'title': 'Upcomming Events'
    }
    return render(request, 'index.html', context)

@login_required
def dashboard(request):
    user = request.user
    fav_books = user.fav_books.all()

    context = {
        'fav_books': fav_books,
    }
    return render(request, 'dashboard.html', context)

def book_list(request):
    books = Book.objects.all()
    user = request.user

    # search
    form = BookSearchForm(request.GET or None)

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        date_search_query = form.cleaned_data.get('date_search_query')

        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(genres__name__icontains=search_query)
            )

        if date_search_query:
            books = books.filter(published__year=date_search_query)

    books = books.order_by('title')

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user': user,
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'books/book_list.html', context)

class BookCreateView(StaffRequiredMixin,CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_create_form.html'
    success_url = reverse_lazy('book_list')

class BookUpdateView(StaffRequiredMixin,UpdateView):
    model = Book
    form_class = BookEditForm
    template_name = 'books/book_update_form.html'
    success_url = reverse_lazy('book_list')

class BookDeleteView(PermissionRequiredMixin,StaffRequiredMixin,DeleteView):
    permission_required = 'books.delete_book'
    model = Book
    success_url = reverse_lazy('book_list')
    template_name = 'books/book_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookDeleteForm(instance=self.object)
        return context

def book_details(request, pk):
    book = Book.objects.get(pk=pk)
    user = request.user

    # Default: unbound (empty) forms
    comment_form = CommentForm()
    rating_form = RatingForm()

    # coment or rating
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # If comment form was submitted
        if form_type == 'comment':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = user.username if user.is_authenticated else 'Anonymous'
                comment.book = book
                comment.save()
                return redirect('book_details', pk=book.pk)

        # If rating form was submitted
        elif form_type == 'rating' and user.is_authenticated:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                Rating.objects.update_or_create(
                    user=user,
                    book=book,
                    defaults={'score': rating_form.cleaned_data['score']}
                )
                return redirect('book_details', pk=book.pk)

    # user rating
    user_rating = None
    if request.user.is_authenticated:
        rating_obj = Rating.objects.filter(user=request.user, book=book).first() # safe: returns None if no rating instead of throwing an error.
        if rating_obj:
            user_rating = rating_obj.score

    average_rating = book.ratings.aggregate(avg_rating=models.Avg('score'))['avg_rating']
    comments = book.comments.all().order_by('-created_at')

    context = {
        'book': book,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'average_rating': average_rating,
        'user_rating': user_rating,
        'comments': comments,
        'all_genres': book.genres.all(),
    }
    return render(request, 'books/book_details.html', context)

@login_required
def toggle_favorite(request, book_id):
    book = Book.objects.get(pk=book_id)
    user = request.user
    if book in user.fav_books.all():
        user.fav_books.remove(book)
    else:
        user.fav_books.add(book)

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)

    return redirect('book_list')

def subscribe_view(request):
    if request.method == 'POST':
        form = EmailSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            subscriber, created = Subscriber.objects.get_or_create(email=email)

            if created:
                messages.success(request, 'Thanks for subscribing!')
            else:
                messages.error(request, 'You are already subscribed.')
        else:
            messages.error(request, 'Invalid email, please try again.')

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('index')

@login_required
def download_pdf(request,pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.pdf_file:
        raise Http404("No PDF file found.")
    return FileResponse(book.pdf_file.open('rb'), as_attachment=True, filename=book.pdf_file.name)

class MyRedirectView(RedirectView):
    pass