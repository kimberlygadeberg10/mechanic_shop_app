from flask import Blueprint


mechanics_bp = Blueprint("mechanics_bp", __name__)

from app.mechanics import routes
