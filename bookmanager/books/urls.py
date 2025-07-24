from django.urls import path
from . import views
from .views import BookUpdateView, BookDeleteView, MyRedirectView, toggle_favorite, BookCreateView

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),

    path('create/', BookCreateView.as_view(), name='book_create'),
    path('edit/<int:pk>/', BookUpdateView.as_view(), name='book_edit'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),

    path('details/<int:pk>/', views.book_details, name='book_details'),

    path('books/<int:book_id>/favorite/', toggle_favorite, name='toggle_favorite'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('download/<int:pk>/', views.download_pdf, name='book_download'),
    path('github/', MyRedirectView.as_view(url='https://github.com/PamelaPeneva', permanent=False), name='github-redirect'),

]
