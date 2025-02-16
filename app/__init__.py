import os
from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

from app.main import *
from app.auth import *
from app.memories import *
from app.ai import *