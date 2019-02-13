from django.core.management.base import BaseCommand

from value.deliverables.meetings.models import Meeting


class Command(BaseCommand):
    help = 'Update meeting progress and rankings.'

    def handle(self, *args, **kwargs):
        meetings = Meeting.objects.all()
        for meeting in meetings:
            self.stdout.write(u'Updating meeting "%s"...\n' % meeting.name)
            meeting.calculate_progress()
            meeting.calculate_all_rankings()
        self.stdout.write(self.style.SUCCESS('Meetings stats synced with success!'))

