from flask import Blueprint

from flask.ext.login import login_required, current_user
from flask import render_template, abort
from app.models import Monkey
from app.forms import RegistrationForm
from config import ITEMS_PER_PAGE

from app.models import db

monkeys = Blueprint(
    'monkeys', 
    __name__,
    template_folder='../templates/monkeys'
)


@monkeys.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')


@monkeys.route('/monkeys', methods=['GET'])
@monkeys.route('/monkeys/p/<int:page>', methods=['GET'])
@login_required
def list_monkeys(page=1):
    pagination = Monkey.query.filter_by(is_public=True) \
                             .paginate(page, ITEMS_PER_PAGE)
    return render_template('monkeys.html', pagination=pagination)


@monkeys.route('/monkeys/<int:id>', methods=['GET'])
@login_required
def show_monkey(id):
    monkey = Monkey.query.get_or_404(id)
    return render_template('monkey.html', monkey=monkey)


@monkeys.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    pass
