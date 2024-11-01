# upcoming_event/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from calendar import monthrange, weekday, SUNDAY
from users.decorators import user_must_be_approved


@login_required
@user_must_be_approved
def event_list(request):
    events = Event.objects.filter(event_date__gte=timezone.now())
    return render(request, 'upcoming_event/event_list.html', {'events': events})

@login_required
def post_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            if event.notify_users:
                send_event_reminders(event)
            return redirect('upcoming_event:event_list')
    else:
        form = EventForm()
    return render(request, 'upcoming_event/post_event.html', {'form': form})

def send_event_reminders(event):
    reminder_time = event.event_date - timedelta(days=3)
    User = get_user_model()  # Get the CustomUser model dynamically
    users = User.objects.all()
    subject = f'Reminder: Upcoming Event "{event.title}"'
    message = f'Hello! This is a reminder for the upcoming event "{event.title}" scheduled on {event.event_date}.'
    recipient_list = [user.email for user in users]
    
    # Check if the event date is in the future and send the reminder
    if timezone.now() < reminder_time:
        for email in recipient_list:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


@login_required
@user_must_be_approved
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'upcoming_event/event_detail.html', {'event': event})

@user_must_be_approved
def calendar(request):
    # Get the requested month and year, default to current
    month = int(request.GET.get('month', timezone.now().month))
    year = int(request.GET.get('year', timezone.now().year))

    # Create a date object for the first day of the month
    first_day = datetime(year, month, 1)
    
    # Get the weekday of the first day (0 = Monday, 6 = Sunday)
    first_weekday = first_day.weekday()
    
    # Get the number of days in the month
    _, num_days = monthrange(year, month)
    
    # Create a list of week lists, each containing day numbers and events
    calendar_weeks = []
    day = 1
    for week in range(6):  # Max 6 weeks in a month
        week_days = []
        for weekday in range(7):
            if (week == 0 and weekday < first_weekday) or (day > num_days):
                week_days.append({'day': '', 'events': []})
            else:
                date = datetime(year, month, day)
                events = Event.objects.filter(event_date__date=date)
                week_days.append({'day': day, 'events': events})
                day += 1
        calendar_weeks.append(week_days)
        if day > num_days:
            break

    # Get all events for the month
    events = Event.objects.filter(
        event_date__year=year,
        event_date__month=month
    ).order_by('event_date')

    context = {
        'calendar_weeks': calendar_weeks,
        'current_month_name': first_day.strftime('%B'),
        'current_year': year,
        'current_day': timezone.now().day if year == timezone.now().year and month == timezone.now().month else None,
        'weekdays': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'events': events,
        'prev_month': (first_day - timedelta(days=1)).month,
        'prev_year': (first_day - timedelta(days=1)).year,
        'next_month': (first_day + timedelta(days=32)).month,
        'next_year': (first_day + timedelta(days=32)).year,
    }

    return render(request, 'upcoming_event/calendar.html', context)

def get_full_name(self):
    names = [self.first_name, self.middle_name, self.last_name]
    return ' '.join(filter(None, names)).strip()
