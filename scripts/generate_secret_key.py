# coding: utf-8

from django.utils.crypto import get_random_string


def main():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    random_string = get_random_string(50, chars)
    print random_string

if __name__ == '__main__':
    main()
