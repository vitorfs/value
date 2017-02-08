# coding: utf-8

from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'value.settings')

import django
django.setup()

from value.deliverables.meetings.models import Meeting


def main():
    meetings = Meeting.objects.all()
    for meeting in meetings:
        meeting.calculate_all_rankings()
    print 'Updated value rankings.'

if __name__ == '__main__':
    main()