from app import app
from app.models import *
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask import request, render_template, jsonify, redirect, g, url_for, abort
from app.forms import *
from app.utils import make_json_resp, DuplicateSuggestionException
from config import ITEMS_PER_PAGE

login_manager = LoginManager()
login_manager.init_app(app)

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
@app.route('/monkeys/p/<int:page>', methods=['GET'])
@login_required
def list_monkeys(page=1):
    pagination = Monkey.query.paginate(page, ITEMS_PER_PAGE)
    return render_template("monkeys.html", pagination=pagination)

@app.route('/monkeys/<int:id>', methods=['GET'])
@login_required
def show_monkey(id):
    monkey = Monkey.query.get(id)
    if monkey is None:
        abort(404)
    return render_template("monkey.html", monkey=monkey)

@app.route('/edit_profile', methods=['GET', 'POST'])    # /monkeys/<int:id>/edit
@login_required
def edit_profile():
    pass

@app.route('/ideas', methods=['GET'])
@app.route('/ideas/p/<int:page>', methods=['GET'])
@login_required
def list_ideas(page=1):
    pagination = Idea.query.paginate(page, ITEMS_PER_PAGE)
    return render_template("ideas.html", pagination=pagination)

@app.route('/ideas/<int:id>', methods=['GET'])
@login_required
def show_idea(id):
    idea = Idea.query.get(id)
    if idea is None:
        abort(404)
    return render_template("idea.html", idea=idea)

@app.route('/ideas/new', methods=['GET', 'POST'])
@login_required
def add_idea():
    form = IdeaForm()
    form.status_id.choices = [(s.id, s.name) for s in IdeaStatus.query.all()]
    form.fields.choices = [(f.id, f.name) for f in Field.query.all()]
    
    if request.method == 'GET':
        return render_template('idea_form.html', form=form)
    
    if not form.validate_on_submit():
        return make_json_resp(400, **form.errors)
    
    i = Idea(form.title.data, form.body.data, current_user.id, form.is_public.data)
    i.status_id = form.status_id.data
    i.fields = Field.query.filter(Field.id.in_(form.fields.data)).all()
    db.session.add(i)
    db.session.commit()
    
    return make_json_resp(200, redirect=url_for('show_idea', id=i.id))

@app.route('/ideas/<int:id>/edit', methods=['GET'])
@login_required
def edit_idea(id):
    pass

@app.route('/monkeys/<int:monkey_id>/suggest', methods=['GET', 'POST'])
@login_required
def suggest_to_user(monkey_id):
    monkey = Monkey.query.get(monkey_id)
    if monkey is None:
        abort(404)
        
    form = SuggestForm()
    ideas = current_user.get_ideas_to_suggest(monkey)
    form.idea_id.choices = [(i.id, i.title) for i in ideas]
    
    if request.method == 'GET':
        return render_template("suggest_form.html", form=form, monkey=monkey)
    
    if not form.validate_on_submit():
        return make_json_resp(400, **form.errors)
    
    try:
        suggestion = Suggestion(monkey.id, form.idea_id.data)
    except DuplicateSuggestionException:
        return make_json_resp(400, idea_id="This idea was already suggested to this monkey")
    else:
        db.session.add(suggestion)
        db.session.commit()
        return make_json_resp(200, redirect=url_for('list_monkeys'))
    
@app.route('/ideas/<int:idea_id>/join', methods=['GET', 'POST'])
@login_required
def request_to_join(idea_id):
    idea = Idea.query.get(idea_id)
    if idea is None:
        abort(404)
    
    form = JoinRequestForm()
    
    if request.method == 'GET':
        return render_template("join_form.html", form=form, idea=idea)
    
    if not form.validate_on_submit():
        return make_json_resp(400, **form.errors)
    
    try:
        join = JoinRequest(current_user, idea, form.message.data)
    except Exception as e:
        return make_json_resp(400, message=e.message)
    else:
        db.session.add(join)
        db.session.commit()
        return make_json_resp(200, redirect=url_for('list_ideas'))

@app.route('/requests', methods=['GET'])
@login_required
def list_join_requests():
    ideas = Idea.query.filter_by(author_id=current_user.id)
    return render_template("join_requests.html", ideas=ideas)

@app.route('/suggestions', methods=['GET'])
@login_required
def list_suggestions():
    return render_template("suggestions.html")

@app.route('/requests/<int:id>/<string:action>', methods=['POST'])
@login_required
def accept_decline_request(id, action):
    if action != 'accept' and action != 'decline':
        return make_json_resp(400, error="Wrong action")
    
    jr = JoinRequest.query.get(id)
    if jr is None:
        abort(404)
    
    if jr.idea.author_id != current_user.id:
        return make_json_resp(403, error="Not authorized")
    
    jr.status = JoinRequestStatus.ACCEPTED if action == 'accept' else JoinRequestStatus.DECLINED
    if action == 'accept':
        jr.idea.monkeys.append(jr.monkey)
    db.session.commit()
    
    return make_json_resp(200)