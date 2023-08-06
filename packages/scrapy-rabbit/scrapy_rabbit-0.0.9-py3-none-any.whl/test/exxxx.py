# -*- coding: utf-8 -*-
from scrapy_rabbit.cmdline import execute
execute()
from test import default_settings

# for name in dir(default_settings):
#     if name.isupper():
#         print(name, getattr(default_settings, name))
# import os
#
# ENVVAR = 'SCRAPY_SETTINGS_MODULE'
# print(os.environ)
#
# if ENVVAR not in os.environ:
#     project = os.environ.get('SCRAPY_PROJECT', 'default')
#     print(project, type(project))
