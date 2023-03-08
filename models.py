"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "/static/default_image.png"

def connect_db(app):
    """Connect this database to the provided Flask app.
    It should be called from the Flask app.
    """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(20),
                           nullable=False)
                    
    last_name = db.Column(db.String(20),
                           nullable=False)

    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    #cascade='all, delete' - deletes posts when their user is deleted
    # cascade='all, delete-orphan' - also deletes any posts that were "removed" from the 
    # user, even if the user is not deleted
    
                        
    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

    # Full Name Method from SB Solution.
    # You can call this method as a property in the templates.
    # instead of {{ user.first_name }} {{ user.last_name }} can use {{user.full_name}}

    # @property
    # def full_name(self):
    #     """Return full name of user."""

    #     return f"{self.first_name} {self.last_name}"

## Part - 2: Adding Posts

class Post(db.Model):
    """Post Model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text, 
                      nullable=False)

    content = db.Column(db.Text, 
                      nullable=False)

    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)

    # user = db.relationship('Users', backref='posts', cascade="all, delete-orphan")
    # This won't work for delete cascade. i.e When a user is deleted, also delete their posts
    #  Have to define the relationship in the User or it will work reverse

    # or You can give as follows
    # user = relationship('Users', backref=backref("posts", cascade="all, delete-orphan"))

    # Instead we can simply define the relationship in the User Model
    
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>"

    @property
    def friendly_date(self):
        """ Return nicely-formatted date."""

        return self.created_at.strftime("%b %-d  %Y, %-I:%M %p")

        # Mar 7 2023, 12:30 PM
        # %a - Abbr. weekday name like Sun - Not included in this
        # %b - Abbr. Month name like Jan
        # %-d - Abbr. Day of the month as a decimal number like 1, 31
        # %Y - Year like 2023
        # %-I - Hour (12-hour clock) as a decimal number. - 9
        # %M - Minute as a zero-padded decimal number.  - 30
        # %p - Locale’s AM or PM.
