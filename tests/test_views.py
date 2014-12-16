from app.models import *
import pytest
from app.forms import *
from werkzeug.datastructures import MultiDict
from flask import url_for
import json
from flask.ext.login import current_user, login_user, logout_user


@pytest.fixture
def profession(session):
    p = Profession(name='Software Engineer in Test')
    session.add(p)
    session.commit()
    return p
    
    
@pytest.fixture
def password():
    return '123qwe'
    

@pytest.fixture
def monkey(session, profession, password):
    m = Monkey(
        email='crazy@jungles.com', 
        fullname='Jack London', 
        about='Struggling hard in jungles', 
        profession_id=profession.id
    )
    m.set_password(password)
    session.add(m)
    session.commit()
    return m
    

@pytest.fixture
def idea(session, monkey):
    i = Idea(
        title='This is test idea',
        body='Body of the test idea',
        author_id=monkey.id
    )
    session.add(i)
    session.commit()
    return i
    
    
@pytest.fixture
def field(session):
    f = Field(name='Communications')
    session.add(f)
    session.commit()
    return f
    
    
@pytest.fixture
def idea_status(session):
    i = IdeaStatus(name='Demonstration ready')
    session.add(i)
    session.commit()
    return i
    
    
@pytest.fixture
def monkey2(session, monkey, password):
    """Returns a monkey independent from idea fixture
    """
    m = Monkey(
        email='fast@jungles.com', 
        fullname='Tom Sawyer', 
        about='Jungles sharpen skills', 
        profession_id=monkey.profession_id
    )
    m.set_password(password)
    session.add(m)
    session.commit()
    return m
    
    
def post_login(client, email, password):
    data = {
        'email': email,
        'password': password
    }
    client.post(url_for('auth.login'), data=data)
    
        
class TestAuthViews:
    def test_login(self, client, monkey, password):
        with client:
            post_login(client, monkey.email, password)
            assert current_user == monkey
            
    def test_logout(self, client, request_ctx, monkey):
        with client:
            post_login(client, monkey.email, password)
            assert current_user == monkey
            client.post(url_for('auth.logout'))
            assert not current_user.is_authenticated()
            
    def test_register(self, client, profession):
        data = {
            'email': 'test@siroca.com',
            'fullname': 'Testing Registration',
            'password': '123qwe',
            'about': 'a' * 21,
            'profession_id': profession.id
        }
        
        assert Monkey.query.count() == 0
        r = client.post(url_for('auth.register'), data=data)
        assert Monkey.query.count() == 1

        
class TestJoinRequestViews:
    def test_request_to_join(self, client, idea, monkey2, password):
        with client:
            post_login(client, monkey2.email, password)
            assert current_user.is_authenticated()
            assert JoinRequest.query.count() == 0
            data = {
                'message': 'Please, accept this test join request'
            }
            r = client.post(
                url_for('join_requests.request_to_join', idea_id=idea.id), 
                data=data
            )
            assert JoinRequest.query.count() == 1


class TestIdeaViews:
    def test_add_new_idea(self, client, monkey, 
                          password, field, idea_status):
        with client:
            post_login(client, monkey.email, password)
            data = {
                'title': 'This is test idea',
                'body': 'This is test body',
                'is_public': True,
                'fields': [field.id],
                'status_id': idea_status.id
            }
            r = client.post(url_for('ideas.add_idea'), data=data)
            print r
            print r.data
            assert Idea.query.count() == 1
            
    def test_accept_request(self, client, session, idea, monkey2, password):
        jr = JoinRequest(monkey2, idea)
        session.add(jr)
        session.commit()
        with client:
            post_login(client, idea.author.email, password)
            r = client.post(
                url_for(
                    'join_requests.accept_decline_request', 
                    id=jr.id, 
                    action='accept'
                )
            )
            assert r.status_code == 200
        
            
class TestSuggestionViews:
    def test_suggest_to_user(self, client, idea, monkey2, password):
        with client:
            post_login(client, idea.author.email, password)
            data = {
                'idea_id': idea.id
            }
            r = client.post(
                url_for(
                    'suggestions.suggest_to_user', 
                    monkey_id=monkey2.id
                ), 
                data=data, 
                follow_redirects=True
            )
            assert r.status_code == 200
            assert Suggestion.query.count() == 1
