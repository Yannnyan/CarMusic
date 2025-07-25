""" This module ties the configuration to the behaviour of the modules """
import hashlib
import os
import encodings


HASH_ALGO = getattr(hashlib, os.environ.get("ENCRYPTION_ALGO"))
ENC_MODULE = getattr(encodings, os.environ.get("ENCODING"))
YOUTUBE_STREAM_AUDIO = os.environ.get("YOUTUBE_STREAM_AUDIO")
DOWNLOAD_DESTINATION = os.environ.get("DOWNLOAD_DESTINATION")
CONVERT_SCRIPT_PATH  = os.environ.get("CONVERT_SCRIPT_PATH")
