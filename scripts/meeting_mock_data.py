# coding: utf-8

from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'value.settings')

import django
django.setup()


import random
from django.utils import timezone
from value.deliverables.meetings.models import Meeting, Evaluation


def main(argv=sys.argv):
    if len(argv) > 1:
        meeting_id = argv[1]
        meeting = Meeting.objects.get(pk=meeting_id)
        meeting.evaluation_set.all().delete()

        measure = meeting.deliverable.measure
        measure_values = list(measure.measurevalue_set.all())

        if len(argv) > 2:
            pseudo_random_push = int(argv[2])

        max_rand = len(measure_values) - 1
        if max_rand >= 0:
            for stakeholder in meeting.meetingstakeholder_set.all():
                for meeting_item in meeting.meetingitem_set.all():
                    for factor in meeting.deliverable.factors.all():
                        if pseudo_random_push:
                            measure_value_index = random.randint(0, max_rand)
                            if measure_value_index == pseudo_random_push:
                                measure_value_index = random.randint(0, max_rand)
                        else:
                            measure_value_index = random.randint(0, max_rand)
                        Evaluation.objects.create(
                            meeting=meeting,
                            meeting_item=meeting_item,
                            user=stakeholder.stakeholder,
                            factor=factor,
                            measure=measure,
                            measure_value=measure_values[measure_value_index],
                            evaluated_at=timezone.now()
                            )
                    meeting_item.calculate_ranking()
    else:
        print('Not enough arguments.')

if __name__ == '__main__':
    main()