import pytest
import json
import os
import importlib
import pprint
import json
import logging
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK

from baserow_vocabai_plugin.cloudlanguagetools import clt_interface, quotas
import cloudlanguagetools.languages

logger = logging.getLogger(__name__)

# tests which need to be run with CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES=yes

def use_clt_test_services():
    os.environ['CLOUDLANGUAGETOOLS_CORE_TEST_SERVICES'] = 'yes'
    importlib.reload(cloudlanguagetools.servicemanager)
    clt_interface.reload_manager()    
    


