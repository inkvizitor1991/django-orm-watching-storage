import django
from django.utils.timezone import localdate

from datacenter.models import Visit
from django.shortcuts import render
from .models import get_duration
from .models import format_duration
from .models import is_visit_long


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    minutes = 60
    non_closed_visits = []
    for visit in visits:
        arrival_date = visit.entered_at
        visitor_name = visit.passcard
        date_now = django.utils.timezone.localtime()
        duration_seconds = get_duration(arrival_date, date_now)
        location_time = format_duration(duration_seconds)
        visit_long = is_visit_long(duration_seconds, minutes)
        arrival_date = visit.entered_at
        non_closed_visits.append(
            {
                'who_entered': visitor_name,
                'entered_at': arrival_date,
                'duration': location_time,
                'is_strange': visit_long,
            }
        )

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
