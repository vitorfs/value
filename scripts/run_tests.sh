#!/bin/bash

flake8 value
coverage run manage.py test --settings=value.test_settings --verbosity=2
coverage html
