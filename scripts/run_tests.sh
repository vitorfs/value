#!/bin/bash

pep8 --exclude=migrations value
coverage run --source=. --omit='*migrations*' manage.py test --settings=value.test_settings --verbosity=2
