from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('flasker.setting')    #模块下的setting文件名，不用加py后缀

#db = SQLAlchemy(app)

from flasker.controller import blog_message