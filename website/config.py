from flask import Blueprint, render_template
config = Blueprint("config", __name__)

@config.errorhandler(404)
def not_found(e):
  return render_template("404.html")