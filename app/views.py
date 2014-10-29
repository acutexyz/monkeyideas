from app import app
from app.models import *
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask import request, render_template, jsonify, redirect, g, url_for
from app.forms import *
from app.utils import make_json_resp
from config import ITEMS_PER_PAGE

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userId):
    return Monkey.query.get(userId)

@app.before_request
def before_request():
    g.user = current_user
    
@app.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template("login_form.html", form=form)
    
    if form.validate_on_submit():
        user = Monkey.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            return make_json_resp(400, email=['Wrong username or password'])
        
        login_user(user)
        return make_json_resp(200, redirect=(request.args.get("next") or url_for('home')))
    else:
        return make_json_resp(400, **form.errors)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    form.profession_id.choices = [(p.id, p.name) for p in Profession.query.all()]
    
    if request.method == 'GET':
        return render_template('register_form.html', form=form)
    
    if not form.validate_on_submit():
        return make_json_resp(400, **form.errors)
    
    if Monkey.query.filter_by(email=form.email.data).count() > 0:
        return make_json_resp(400, email=['This email has been already registered']) # todo: move this to wtf validation
    monkey = Monkey(form.email.data, form.fullname.data, form.about.data, form.profession_id.data)
    monkey.set_password(form.password.data)
    db.session.add(monkey)
    db.session.commit()
    
    return make_json_resp(200, redirect=url_for('login'))

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
@app.route('/ideas/p/<int:page>', methods=['GET'])
@login_required
def list_ideas(page=1):
    print(page)
    pagination = Idea.query.paginate(page, ITEMS_PER_PAGE)
    print(ITEMS_PER_PAGE)
    print(pagination.items)
    return render_template("ideas.html", pagination=pagination)

@app.route('/ideas/<int:id>', methods=['GET'])
@login_required
def show_idea(id):
    pass

@app.route('/ideas/new', methods=['GET', 'POST'])
@login_required
def add_idea():
    form = IdeaForm()
    form.status_id.choices = [(s.id, s.name) for s in IdeaStatus.query.all()]
    form.fields.choices = [(f.id, f.name) for f in Field.query.all()]
    
    if request.method == 'GET':
        return render_template('idea_form.html', form=form)
    
    print(request.form)
    print(form.fields.data)
    
    if not form.validate_on_submit():
        return make_json_resp(400, **form.errors)
    
    return make_json_resp(200, redirect=url_for('show_idea', id=1))

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