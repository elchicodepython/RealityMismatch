from django.urls import path as level_url


"""Importing level_url from this package instead of importing path from django
make us the possibility of change the framework in the future implementing
path interface for the new framework in this module and setting it to level_url
without making breaking changes
"""
