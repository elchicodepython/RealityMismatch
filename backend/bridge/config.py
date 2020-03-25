from django.conf import settings

"""Empty configuration file just to be loosly coupled to django or other
framework configuration.

Other apps can get configuration elements importing conf variable name from
this module.

eg. `from core.config import conf`

"""

class Conf:
    def __getitem__(self, key):
        value = getattr(settings, key)
        if not value:
            raise KeyError
        return value


conf = Conf()