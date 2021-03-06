from flask import Blueprint

from app.models import Suggestion, Monkey
from flask.ext.login import login_required, current_user
from flask import (
    request, 
    render_template, 
    redirect, 
    url_for, 
    abort
)
from app.forms import SuggestForm
from app.utils import make_json_resp, DuplicateSuggestionError

from app.models import db

suggestions = Blueprint(
    'suggestions', 
    __name__,
    template_folder='../templates/suggestions'
)


@suggestions.route(
    '/monkeys/<int:monkey_id>/suggest', 
    methods=['GET', 'POST']
)
@login_required
def suggest_to_user(monkey_id):
    monkey = Monkey.query.get_or_404(monkey_id)
        
    form = SuggestForm()
    form.idea_id.query = current_user.get_ideas_to_suggest(monkey)

    if request.method == 'GET':
        return render_template(
            'suggest_form.html', 
            form=form, 
            monkey=monkey
        )
    
    if not form.validate_on_submit():
        return make_json_resp(400, **form.errors)
    
    try:
        suggestion = Suggestion(monkey.id, form.idea_id.data.id)
    except DuplicateSuggestionError:
        return make_json_resp(
            400, 
            idea_id='This idea was already suggested to this monkey'
        )
    except Exception as e:
        return make_json_resp(400, idea_id=e.message)
    else:
        db.session.add(suggestion)
        db.session.commit()
        return make_json_resp(200, redirect=url_for('monkeys.list_monkeys'))
    

@suggestions.route('/suggestions', methods=['GET'])
@login_required
def list_suggestions():
    return render_template('suggestions.html')
