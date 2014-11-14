from flask import Blueprint

from flask.ext.login import login_required, current_user
from flask import request, render_template, redirect, url_for, abort
from app.models import Field, Idea, IdeaStatus
from app.forms import IdeaForm
from app.utils import make_json_resp
from config import ITEMS_PER_PAGE

from app.models import db

ideas = Blueprint('ideas', __name__, template_folder='../templates/ideas')

@ideas.route('/ideas', methods=['GET'])
@ideas.route('/ideas/p/<int:page>', methods=['GET'])
@login_required
def list_ideas(page=1):
    pagination = Idea.query.paginate(page, ITEMS_PER_PAGE)
    return render_template("ideas.html", pagination=pagination)

@ideas.route('/ideas/<int:id>', methods=['GET'])
@login_required
def show_idea(id):
    idea = Idea.query.get(id)
    if idea is None:
        abort(404)
    return render_template("idea.html", idea=idea)

@ideas.route('/ideas/new', methods=['GET', 'POST'])
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
    
    return make_json_resp(200, redirect=url_for('ideas.show_idea', id=i.id))

@ideas.route('/ideas/<int:id>/edit', methods=['GET'])
@login_required
def edit_idea(id):
    pass