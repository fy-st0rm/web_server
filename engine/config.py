# Imports
import socket
import threading
import json
import os
import sys
import time
import datetime
import uuid

from .keywords import *

FORMAT = "utf-8"

# Directory where the websites lies
WEB_DIR = "web"
IMG_DIR = "image"
ROOT_FILE = "index.html"

# Database constants
DATABASE_DIR = ".sv_data"

# Objects
USERS     = "users.json"
CATEGORY = "category.json"
POSTS     = "posts.json"
COMMENTS  = "comments.json"

