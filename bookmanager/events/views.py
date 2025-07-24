from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone

from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView,DeleteView

from accounts.mixins import StaffRequiredMixin
from events.forms import EventCreateForm
from events.models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list_page.html'
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['time'] = timezone.now()
        context['title'] = 'Events'
        return context

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     kwargs.update({
    #         'time': timezone.now(),
    #         'title': 'All Events',
    #     })
    #     return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        return Event.objects.order_by('-start_time')

class EventDetailsView(DetailView):
    model = Event
    template_name = 'events/event_details.html'
    context_object_name = 'event'

class EventCreateView(StaffRequiredMixin,CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'events/event_create.html'
    success_url = reverse_lazy('event_list')

class EventDeleteView(PermissionRequiredMixin,StaffRequiredMixin,DeleteView):
    permission_required = 'events.delete_event'
    model = Event
    template_name = 'events/event_delete.html'
    success_url = reverse_lazy('event_list')