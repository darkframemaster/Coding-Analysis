#!/usr/bin/env python3.5

import os

from flask  import Flask

# Init app and database
app = Flask(__name__)
app.config.from_object('flask_config')

# After init app and db import views and models
from . import views

