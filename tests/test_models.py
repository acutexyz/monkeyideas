from app.models import *
from app.utils import DuplicateSuggestionError
import pytest
from app.forms import *
from werkzeug.datastructures import MultiDict
from utils import create_idea_by_monkey


@pytest.fixture(scope='function')
def profession(session):
    p = Profession(name='Software Engineer in Test')
    session.add(p)
    session.commit()
    return p
        
        
@pytest.fixture(scope='function')
def monkey(session, profession):
    m = Monkey(
        email='crazy@jungles.com', 
        fullname='Jack London', 
        about='Struggling hard in jungles', 
        profession_id=profession.id
    )
    session.add(m)
    session.commit()
    return m
    
    
@pytest.fixture(scope='function')
def two_monkeys(session, monkey):
    monkey2 = Monkey(
        email='fast@jungles.com', 
        fullname='Tom Sawyer', 
        about='Jungles sharpen skills', 
        profession_id=monkey.profession_id
    )
    session.add(monkey2)
    session.commit()
    
    return (monkey, monkey2)
    
    
class TestJoinRequest:
    def test_author(self, session, monkey):
        """Make sure that author of an idea can not 
        joinrequest his/her own idea
        """
        idea = create_idea_by_monkey(session, monkey)
        
        with pytest.raises(Exception) as ei:
            join_request = JoinRequest(monkey, idea)      
        assert ei.value.message == 'Author can not join own idea'
        
    def test_already_requested(self, session, two_monkeys):
        """Make sure that monkey can not joinrequest twice while 
       previous request hasn't been accepted or declined.
        """
        monkey, monkey2 = two_monkeys
        idea = create_idea_by_monkey(session, monkey)
        
        join_request = JoinRequest(monkey2, idea)
        session.add(join_request)
        session.commit()
        
        with pytest.raises(Exception) as ei:
            join_request2 = JoinRequest(monkey2, idea)
        assert ei.value.message == 'Monkey had already requested ' + \
                                   'to join this idea'
        
    def test_member(self, session, two_monkeys):
        """Check that member of an idea can not joinrequest this idea
        """
        monkey, monkey2 = two_monkeys
        idea = create_idea_by_monkey(session, monkey)
        
        idea.add_member(monkey2)
        session.commit()
        
        with pytest.raises(Exception) as ei:
            join_request = JoinRequest(monkey2, idea)        
        assert ei.value.message == 'Monkey is already member of this idea'
    
    
class TestIdea:
    def test_member_author(self, session, monkey):
        """Make sure that author of an idea can not be added as a member
        """
        idea = create_idea_by_monkey(session, monkey)
        
        with pytest.raises(Exception) as ei:
            idea.add_member(monkey)
        assert ei.value.message == 'Author can not become member of an idea'
        
    def test_already_member(self, session, two_monkeys):
        """Assert that present member can not be added to members once more
        """
        monkey, monkey2 = two_monkeys
        idea = create_idea_by_monkey(session, monkey)
        
        idea.add_member(monkey2)
        session.commit()
        
        with pytest.raises(Exception) as ei:
            idea.add_member(monkey2)
        assert ei.value.message == 'Monkey is already a member'
    
    
class TestSuggestion:
    def test_one_suggest_only(self, session, two_monkeys):
        """Check that an idea can be suggested to a 
        particular monkey only once
        """
        monkey, monkey2 = two_monkeys
        idea = create_idea_by_monkey(session, monkey)
        
        suggestion = Suggestion(monkey2.id, idea.id)
        session.add(suggestion)
        session.commit()
        
        with pytest.raises(DuplicateSuggestionError):
            suggestion2 = Suggestion(monkey2.id, idea.id)
