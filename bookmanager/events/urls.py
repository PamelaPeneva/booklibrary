
from django.urls import path


from events.views import EventCreateView, EventDetailsView, EventListView, EventDeleteView

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('details/<int:pk>/', EventDetailsView.as_view(), name='event_details'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),

]