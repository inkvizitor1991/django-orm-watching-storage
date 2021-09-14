from django.db import models


def is_visit_long(duration_seconds, minutes=60):
    visit_long = bool(duration_seconds // (minutes * 60))
    return visit_long


def get_duration(arrival_date, exit_date):
    delta = exit_date - arrival_date
    duration_seconds = delta.total_seconds()
    return duration_seconds


def format_duration(duration_seconds):
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    location_time = f'{hours} ч: {minutes} мин'
    return location_time


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved='leaved at ' + str(
                self.leaved_at) if self.leaved_at else 'not leaved'
        )
