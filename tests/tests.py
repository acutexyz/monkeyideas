from app.models import *
from app.utils import DuplicateSuggestionException
import pytest

def create_new_monkeys(session):
    """Creates and returns a new monkey.
    Since monkey is bound to a profession, it also 
    creates a new profession if there is no one.
    """
    profession = Profession.query.first()
    if profession is None:
        profession = Profession("Monkey Tester")
        session.add(profession)
        session.commit()
    
    monkeys = [Monkey("crazy@jungles.com", "Jack London", "Struggling hard in jungles", 
                    profession.id), Monkey("fast@jungles.com", "Tom Sawyer", "Jungles sharpen skills", 
                                          profession.id)]
    for monkey in monkeys:
        session.add(monkey)
    session.commit()
    
    return (monkeys[0], monkeys[1])

def create_idea_by_monkey(session, monkey):
    """Creates and returns new idea authored by given monkey
    """
    idea = Idea("-", "-", monkey.id, True) # author is monkey
    session.add(idea)
    session.commit()
    return idea

#
# Tests for JoinRequest
#
    
def test_author(session):
    """Make sure that author of an idea can't 
    request to join his/her own idea
    """
    monkey = create_new_monkeys(session)[0]
    idea = create_idea_by_monkey(session, monkey)
    
    with pytest.raises(Exception) as ei:
        join_request = JoinRequest(monkey, idea)      
    assert ei.value.message == "Author can't join own idea"
    
def test_already_requested(session):
    """Make sure that monkey can't joinrequest twice while 
   previous request hasn't been accepted or declined)
    """
    monkey, monkey2 = create_new_monkeys(session)
    idea = create_idea_by_monkey(session, monkey)
    
    join_request = JoinRequest(monkey2, idea)
    session.add(join_request)
    session.commit()
    
    with pytest.raises(Exception) as ei:
        join_request2 = JoinRequest(monkey2, idea)
    assert ei.value.message == "Monkey had already requested to join this idea"
    
def test_member(session):
    """Check that member of an idea can't request to join an idea
    """
    monkey, monkey2 = create_new_monkeys(session)
    idea = create_idea_by_monkey(session, monkey)
    
    idea.add_member(monkey2)
    session.commit()
    
    with pytest.raises(Exception) as ei:
        join_request = JoinRequest(monkey2, idea)        
    assert ei.value.message == "Monkey is already member of this idea"
    
    
#
# Tests for Idea
#

def test_member_author(session):
    """Make sure that author of an idea can't be added as member
    """
    monkey = create_new_monkeys(session)[0]
    idea = create_idea_by_monkey(session, monkey)
    
    with pytest.raises(Exception) as ei:
        idea.add_member(monkey)
    assert ei.value.message == "Author can't become member of an idea"
    
def test_already_member(session):
    """Assert that present member can't be added to members once more
    """
    monkey, monkey2 = create_new_monkeys(session)
    idea = create_idea_by_monkey(session, monkey)
    
    idea.add_member(monkey2)
    session.commit()
    
    with pytest.raises(Exception) as ei:
        idea.add_member(monkey2)
    assert ei.value.message == "Monkey is already a member"
    
    
#
# Tests for Suggestions
#

def test_one_suggest_only(session):
    """Check that an idea can be suggested to a particular monkey only once
    """
    monkey, monkey2 = create_new_monkeys(session)
    idea = create_idea_by_monkey(session, monkey)
    
    suggestion = Suggestion(monkey2.id, idea.id)
    session.add(suggestion)
    session.commit()
    
    with pytest.raises(DuplicateSuggestionException):
        suggestion2 = Suggestion(monkey2.id, idea.id)