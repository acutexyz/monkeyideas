from flask import Blueprint

from app.models import Idea, JoinRequest, JoinRequestStatus
from flask.ext.login import login_required, current_user
from flask import request, render_template, redirect, url_for, abort
from app.forms import JoinRequestForm
from app.utils import make_json_resp

join_requests = Blueprint('join_requests', __name__, template_folder='../templates/join_requests')

from app.models import db

@join_requests.route('/ideas/<int:idea_id>/join', methods=['GET', 'POST'])
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
        return make_json_resp(200, redirect=url_for('ideas.list_ideas'))

@join_requests.route('/requests', methods=['GET'])
@login_required
def list_join_requests():
    ideas = Idea.query.filter_by(author_id=current_user.id)
    return render_template("join_requests.html", ideas=ideas)

@join_requests.route('/requests/<int:id>/<string:action>', methods=['POST'])
@login_required
def accept_decline_request(id, action):
    if action != 'accept' and action != 'decline':
        return make_json_resp(400, error="Wrong action")
    
    jr = JoinRequest.query.get(id)
    if jr is None:
        abort(404)
    
    if jr.idea.author_id != current_user.id:
        return make_json_resp(403, error="Not authorized")
    
    if action == 'accept':
        jr.status = JoinRequestStatus.ACCEPTED
        jr.idea.add_member(jr.monkey)
    elif action == 'decline':
        jr.status = JoinRequestStatus.DECLINED
    
    db.session.commit()
    
    return make_json_resp(200)