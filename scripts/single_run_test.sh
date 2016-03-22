#!/bin/bash

coverage run manage.py test $1 --settings=value.test_settings --verbosity=2
coverage html
