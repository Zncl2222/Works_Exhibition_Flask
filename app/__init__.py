from flask import Flask

app = Flask(__name__)

from app.model import UC_SGSIM_py

from app.controllor import route
from app.controllor import uc_sgsim_py_controllor
from app.controllor import db_controllor

