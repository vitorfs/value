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
    for m in meetings:
        m.calculate_progress()
    print 'Calculate progress done.'

if __name__ == '__main__':
    main()