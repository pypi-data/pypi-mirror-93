import logging
from logging import NullHandler
# Set default logging handler to avoid "No handler found" warnings.
# from toolkit_w.internal import vars_global
# from toolkit_w.resources import *
from toolkit_w.whatify_toolkit import MyWhatify

from fireflyai import enums
from fireflyai.token_json import UserToken
from fireflyai.resources import *


logger = logging.getLogger(__name__)
token = None
user_token = None



