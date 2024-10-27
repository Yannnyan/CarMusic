""" This module links the configuration to the behaviour of the modules """
import encodings
import hashlib
import os
import encodings
from env import *

hash_algo = getattr(hashlib, os.environ.get("ENCRYPTION_ALGO"))
enc_module = getattr(encodings, os.environ.get("ENCODING"))
