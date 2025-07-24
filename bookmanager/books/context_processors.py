from .forms import EmailSubscriptionForm

def subscription_form(request):
    return {
        'subscribe_form': EmailSubscriptionForm()
    }

