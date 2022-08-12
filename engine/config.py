# Imports
import socket
import threading
import json
import os
import sys
import time
import base64
import re

from .keywords import *

FORMAT = "utf-8"

# Directory where the websites lies
WEB_DIR = "web"
ROOT_FILE = "index.html"

# Database constants
DATABASE_DIR = ".sv_data"

