from app.models import *
import pytest
from app.forms import *
from werkzeug.datastructures import MultiDict


@pytest.fixture(scope='function')
def profession(session):
	p = Profession(name="Software Engineer in Test")
	session.add(p)
	session.commit()
	return p
		
		
@pytest.fixture(scope='function')
def monkey(session, profession):
	m = Monkey(
        email="crazy@jungles.com", 
        fullname="Jack London", 
        about="Struggling hard in jungles", 
        profession_id=profession.id
    )
	session.add(m)
	session.commit()
	return m
	

class TestRegistrationForm:
	def test_uq_email(self, monkey):
		data = MultiDict([
			('email', monkey.email)
		])
		form = RegistrationForm(data, csrf_enabled=False)
		assert not form.validate()
		assert form.errors['email'] == \
			['This email has been already registered']
		
	def test_max(self):
		data = MultiDict([
			('fullname', "s" * 101),
			('password', "s" * 21),
			('about', "s" * 201)
		])
		form = RegistrationForm(data, csrf_enabled=False)
		assert not form.validate()
		assert form.errors['password'] == \
			['Field must be between 6 and 20 characters long.']
		assert form.errors['fullname'] == \
			['Field must be between 5 and 100 characters long.']
		assert form.errors['about'] ==	\
			['Field must be between 20 and 200 characters long.']
		

class TestSuggestForm:
	def test_empty_submit(self):
		form = SuggestForm(csrf_enabled=False)
		assert not form.validate()
		
		assert form.errors == {
			'idea_id': ['This field is required.']
		}


class TestLoginForm:		
	def test_valid_login(self):
		data = MultiDict([
			('email', 'aidanxyz@gmail.com'),
			('password', '123qwe')
		])
		form = LoginForm(data, csrf_enabled=False)
		assert form.validate()
		assert form.errors == {}

	def test_empty_submit(self):
		form = LoginForm(csrf_enabled=False)
		assert not form.validate()
	
		assert form.errors == {
			'email': ['This field is required.'],
			'password': ['This field is required.']
		}
	
	def test_valid_login(self):
		data = MultiDict([
			('email', 'aidanxyz@gmail.com'),
			('password', '123qwe')
		])
		form = LoginForm(data, csrf_enabled=False)
		assert form.validate()
		assert form.errors == {}
	
	def test_email_field(self):
		data = MultiDict([
			('email', 'this_is_not_valid_email@')
		])
		form = LoginForm(data, csrf_enabled=False)
		assert not form.validate()
	
		assert form.errors['email'] == ['Invalid email address.']
