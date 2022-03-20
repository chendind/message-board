from app import db
from app.models import User, Comment

def getParentComment(parent_comment_id):
    return Comment.query.filter(Comment.id == parent_comment_id).first()

def addComment(user_id, content, parent_comment_id, ancestor_comment_id):
    comment = Comment(user_id = user_id, content = content, parent_comment_id = parent_comment_id, ancestor_comment_id = ancestor_comment_id)
    db.session.add(comment)
    db.session.commit()
    return comment

def getCommentsJoinWithUser():
    return db.session.query(Comment, User).outerjoin(User, User.id == Comment.user_id).order_by(Comment.id.desc()).all()