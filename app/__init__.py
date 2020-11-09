from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
	app = Flask(__name__, instance_relative_config=False)
	if app.config["ENV"] == "production":
		app.config.from_object("config.ProductionConfig")
		print("ENV: Production")
	elif app.config["ENV"] == "testing":
		app.config.from_object("config.TestingConfig")
		print("ENV: Testing")
	else:
		app.config.from_object("config.DevelopmentConfig")
		print("ENV: Development")

	db.init_app(app)

	with app.app_context():
		# get rountes
		from . import views
		from . import user_views
		from . import routes

		db.create_all()

		return app 
