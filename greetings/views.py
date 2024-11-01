# greetings/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Greeting

class GreetingListView(LoginRequiredMixin, ListView):
    model = Greeting
    template_name = 'greetings/greeting_list.html'
    context_object_name = 'greetings'

    def get_queryset(self):
        return Greeting.objects.filter(user=self.request.user).select_related('user')
