from django.core.exceptions import ObjectDoesNotExist

from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from .models import get_duration
from .models import format_duration
from .models import is_visit_long


def passcard_info_view(request, passcode):
    try:
        passcard = Passcard.objects.get(passcode=passcode)
    except ObjectDoesNotExist:
        print("Карточка не найдена")
    active_visit = Visit.objects.filter(passcard=passcard)
    minutes = 60
    this_passcard_visits = []
    for visit in active_visit:
        exit_date = visit.leaved_at
        arrival_date = visit.entered_at
        if exit_date:
            duration_seconds = get_duration(arrival_date, exit_date)
            location_time = format_duration(duration_seconds)
            visit_long = is_visit_long(duration_seconds, minutes)
            this_passcard_visits.append(
                {
                    'entered_at': arrival_date,
                    'duration': location_time,
                    'is_strange': visit_long
                },
            )
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
