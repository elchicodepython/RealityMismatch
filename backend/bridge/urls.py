from django.urls import path

from web import urls

"""Importing level_url from this package instead of importing path from django
make us the possibility of change the framework in the future implementing
path interface for the new framework in this module and setting it to level_url
without making breaking changes
"""


def add_url(url_name, url_view):
    """Patch urlpatterns list
    """
    urls.urlpatterns.append(path(url_name, url_view))
