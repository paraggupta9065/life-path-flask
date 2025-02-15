from flask import Flask

app = Flask(__name__)

from app.main import *
from app.auth import *
from app.memories import *