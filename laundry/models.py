import datetime

from flask_login import UserMixin
from flask_sqlalchemy.query import Query
from werkzeug.security import generate_password_hash, check_password_hash

from laundry import db, login_manager



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    accepted_terms = db.Column(db.Boolean(), default=False)
    is_active = db.Column(db.Boolean(), default=True)
    is_superuser = db.Column(db.Boolean(), default=False)
    phone = db.Column(db.String())
    address = db.Column(db.String())

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def password(self) -> AttributeError:
        return {'lol': 'nice try'}

    @password.setter
    def password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)
    
    def get(index: str | int) -> Query | None:
        """ Return a `User` with the given index, either an email or ID.

        :param email: User's email."""
        return User.query.get(index) or User.query.filter_by(email=index).first()


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, index=True)
    amount = db.Column(db.Integer, nullable=False)
    clothes_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.BOOLEAN, default=False)
    service_type = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    pickup_date = db.Column(db.DateTime, nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    pickup_addr = db.Column(db.String, nullable=False)
    delivery_addr = db.Column(db.String, nullable=False)
    reviewed = db.Column(db.BOOLEAN, default=False)
    special_instr = db.Column(db.Text(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_user_id'))

    # Relationships
    user = db.relationship("User", uselist=False, backref="orders")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    message = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_user_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id',
    name='fk_order_id'))

    # Relationships
    user = db.relationship("User", uselist=False, backref="messages")
    order = db.relationship("Order", uselist=False, backref="message")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)



""""SQLAlchemy User loader helper function"""

@login_manager.user_loader
def load_user(id):
    return User.get(id)
