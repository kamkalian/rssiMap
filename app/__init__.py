#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 09:30:12 2018

@author: akurm
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app import routes, model

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')
