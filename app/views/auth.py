from flask import Blueprint

from flask.ext.login import (
    login_user, 
    logout_user,
    login_required, 
    current_user
)
from flask import (
    request, 
    render_template, 
    redirect, 
    url_for
)
from app.models import Profession, Monkey
from app.forms import LoginForm, RegistrationForm
from app.utils import make_json_resp
from app.models import db

auth = Blueprint(
    'auth', 
    __name__, 
    template_folder='../templates/auth'
)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template(
            "login_form.html", 
            form=form
        )
    
    if form.validate_on_submit():
        user = Monkey.query.filter_by(email=form.email.data) \
                           .first()
        if user is None or not user.verify_password(form.password.data):
            return make_json_resp(400, email=[
                    'Wrong username or password'
                ]
            )
        
        login_user(user)
        return make_json_resp(200, redirect=(request.args.get("next") or 
                                             url_for('monkeys.home')))
    else:
        return make_json_resp(400, **form.errors)


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('monkeys.home'))
    
    form = RegistrationForm()
    
    if request.method == 'GET':
        return render_template('register_form.html', form=form)
    
    if not form.validate_on_submit():
        return make_json_resp(400, **form.errors)
    
    monkey = Monkey(
        email=form.email.data, 
        fullname=form.fullname.data, 
        about=form.about.data, 
        profession_id=form.profession_id.data.id
    )
    monkey.set_password(form.password.data)
    db.session.add(monkey)
    db.session.commit()
    
    return make_json_resp(200, redirect=url_for('auth.login'))
