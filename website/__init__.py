from flask import Flask, render_template
import os

def create_app():
	app = Flask(__name__)
	from .inorganica import inorganica
	from .config import config
	#from .admin import admin
	from .train import train
	from .beta import beta
	from .desinorganica import desinorganica
	
	app.register_blueprint(config, url_prefix="/")
	app.register_blueprint(inorganica, url_prefix="/")
	#app.register_blueprint(admin, url_prefix="/admin/")
	app.register_blueprint(train, url_prefix="/")
	app.register_blueprint(beta, url_prefix="/")
	app.register_blueprint(desinorganica, url_prefix="/")
	app.config['SECRET_KEY'] = ('SECRET_KEY')

	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html'), 404
	@app.errorhandler(405)
	def method_not_allowed(e):
		return render_template('405.html'), 405
	@app.errorhandler(500)
	def internal_server_error(e):
		return render_template('500.html'), 500

	return app