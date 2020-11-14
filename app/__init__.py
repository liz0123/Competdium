from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

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
	
	login_manager = LoginManager()
	login_manager.login_view = 'login'
	login_manager.init_app(app)
	
	from .models import User
	
	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	with app.app_context():
		# Include Routes
		from . import routes

		# Register Blueprints
		#app.register_blueprint(auth.auth_bp)
		from . import auth
		
		db.create_all()

		return app 
