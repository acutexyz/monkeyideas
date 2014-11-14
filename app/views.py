from app import app
from app.models import *
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask import request, render_template, jsonify, redirect, g, url_for, abort
from app.forms import *
from app.utils import make_json_resp, DuplicateSuggestionException
from config import ITEMS_PER_PAGE

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userId):
    return Monkey.query.get(userId)

@app.before_request
def before_request():
    g.user = current_user
    if current_user.is_authenticated() and current_user.ideas.count() > 0:
        g.user.join_requests = JoinRequest.query.join(Idea).join(Monkey).filter(Monkey.id==current_user.id, JoinRequest.status==JoinRequestStatus.SENT).count()
    
@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist wrakapakapoufristailo', 404

@app.errorhandler(400)
def custom400(error):
    return error.description, 400