# Imports
import socket
import threading
import json
import os
import sys
import time
import base64
import re

# HTTP Request constants
GET = "GET"
POST = "POST"

# Directory where the websites lies
WEB_DIR = "web"
ROOT_FILE = "index.html"

# Database constants
DATABASE_DIR = ".sv_data"
