# -*- coding: utf-8 -*-
import os
from ...settings import config

def get_prefix_uri(_file_):
    basename = os.path.basename(_file_)
    pname = os.path.splitext(basename)[0]
    ves = os.path.abspath(os.path.dirname(_file_)).split('/')[-1].split('\\')[-1]
    api = '/'.join([config.API_PREFIX,ves,pname])
    return api,ves