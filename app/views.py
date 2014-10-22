from app import app, models
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from flask import request, render_template

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userId):
    return models.Monkey.query.get(userId)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    pass

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    pass

@app.route('/monkeys', methods=['GET'])
@login_required
def list_monkeys():
    pass

@app.route('/monkeys/<int:id>', methods=['GET'])
@login_required
def show_monkey(id):
    pass

@app.route('/edit_profile', methods=['GET', 'POST'])    # /monkeys/<int:id>/edit
@login_required
def edit_profile():
    pass

@app.route('/ideas', methods=['GET'])
@login_required
def list_ideas():
    pass

@app.route('/ideas/<int:id>', methods=['GET'])
@login_required
def show_idea(id):
    pass

@app.route('/ideas/new', methods=['GET', 'POST'])
@login_required
def add_idea():
    pass

@app.route('/ideas/<int:id>/edit', methods=['GET'])
@login_required
def edit_idea(id):
    pass

@app.route('/monkeys/<int:monkey_id>/suggest', methods=['GET', 'POST'])
@login_required
def suggest_to_user(user_id):
    pass

@app.route('/ideas/<int:idea_id>/join', methods=['GET', 'POST'])
@login_required
def request_to_join(idea_id):
    pass