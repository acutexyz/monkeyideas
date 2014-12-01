import os
import pytest

from app.factory import create_app
from app.models import db as _db


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app(os.getcwd() + '/app_config.py')

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def session(app, request):
    """Creates a fresh database and 
    new session for a test.
    """
    _db.app = app
    _db.create_all()
    
    connection = _db.engine.connect()
    
    options = dict(bind=connection)
    session = _db.create_scoped_session(options=options)

    _db.session = session

    def teardown():
        connection.close()
        session.remove()
        _db.drop_all()

    request.addfinalizer(teardown)
    return session
