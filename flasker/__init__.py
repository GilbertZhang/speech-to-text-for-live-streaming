from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('flasker.setting')

from flasker.controller import blog_message