from flask import Flask, g
from flask.ext.login import LoginManager, current_user
from app.models import *

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    
    from app.models import db
        
    login_manager = LoginManager()
    
    from app.views.auth import auth
    from app.views.monkeys import monkeys
    from app.views.ideas import ideas
    from app.views.join_requests import join_requests
    from app.views.suggestions import suggestions
        
    configure_database(app, db)
    configure_login_manager(app, login_manager)
    configure_blueprints(app, [auth, monkeys, ideas, join_requests, suggestions])
    
    return app


def configure_blueprints(app, blueprints):
    """Registers blueprints for given 'app' and 
    associates with @before_request and @errorhandler functions.
    """
    for blueprint in blueprints:
        blueprint.before_request(before_request)
        app.register_blueprint(blueprint)
        
        
def configure_database(app, db):
    """Associates the app with a database object.
    """
    db.init_app(app)
    
    
def configure_login_manager(app, manager):
    """Login manager setup
    """
    manager.init_app(app)
    manager.login_view = "auth.login"
    manager.user_loader(load_user)
    
    
def configure_app(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return 'This page does not exist wrakapakapoufristailo', 404
    
    @app.errorhandler(400)
    def custom400(error):
        return error.description, 400
    
    
def before_request():
    """Sets global user and
    sets the number of join requests that a logged in user has.
    """
    g.user = current_user
    if current_user.is_authenticated() and current_user.ideas.count() > 0:
        g.user.join_requests = JoinRequest.query.join(Idea).join(Monkey).filter(Monkey.id==current_user.id, 
                                                         JoinRequest.status==JoinRequestStatus.SENT).count()
        
        
def load_user(userId):
    """@returns Monkey by given Id.
    This function is used by LoginManager.
    """
    return Monkey.query.get(userId)