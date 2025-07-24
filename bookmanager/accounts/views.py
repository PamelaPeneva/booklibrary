from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm


# def register_view(request):
#     form = CustomUserCreationForm(request.POST or None)
#     if request.method == 'POST' and  form.is_valid():
#         user = form.save()  # save the user
#         login(request, user)  # log the user in immediately
#         messages.success(request, "Account created! You're now logged in.")
#         return redirect('login')
#
#     return render(request, 'accounts/register.html', {'form': form})

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        messages.success(self.request, "Account created! You're now logged in.")
        return redirect(self.get_success_url())





