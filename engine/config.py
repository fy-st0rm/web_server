# Imports
import socket
import threading
import json
import os
import sys
import time

# HTTP Request constants
GET = "GET"
POST = "POST"

# Directory where the websites lies
WEB_DIR = "web"
ROOT_FILE = "index.html"
