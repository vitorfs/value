#!/bin/bash

flake8 value
coverage run manage.py test --settings=value.test_settings --verbosity=1
coverage html
