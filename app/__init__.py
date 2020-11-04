from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")

elif app.config["ENV"] == "testing":

    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from app import views
from app import user_views