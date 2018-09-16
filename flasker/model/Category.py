# from flasker import db
#
# class Category(db.Model):
#     __tablename__ = 'b_category'
#     id = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(20),unique=False)
#     content = db.Column(db.String(100))
#     author = db.Column(db.String(100))
#
#     def __init__(self,title,content,author):
#         self.title = title
#         self.content = content
#         self.author = author
#     def __repr__(self):
#         return '<Category %r>' % self.title