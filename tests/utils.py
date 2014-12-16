from app.models import Idea

def create_idea_by_monkey(session, monkey):
    """Creates and returns new idea authored by given monkey
    """
    idea = Idea(
        title='-', 
        body='-', 
        author_id=monkey.id, 
        is_public=True
    )
    session.add(idea)
    session.commit()
    return idea
