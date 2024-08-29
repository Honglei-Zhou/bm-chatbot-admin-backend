import sqlalchemy_jsonfield
import ujson
import datetime
from database.db_instance import db


class Message(db.Model):
    __tablename__ = 'telle_message'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), nullable=True)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    session_id = db.Column(db.String(120), nullable=False)
    direction = db.Column(db.String(20), nullable=False)
    message = db.Column(
        sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False,
            json=ujson
        ),
        nullable=True
    )

    dialogflow_resp = db.Column(
        sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False,
            json=ujson
        ),
        nullable=True
    )
    is_read = db.Column(db.Integer)
    from_bot = db.Column(db.Integer)
    message_owner = db.Column(db.String(80), nullable=True)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Message %r>' % self.id


class Chat(db.Model):
    __tablename__ = 'telle_chat'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), nullable=True)
    session_id = db.Column(db.String(120), nullable=False)

    device_type = db.Column(db.String(80))
    device_detail = db.Column(db.String(80))

    started = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    duration = db.Column(db.Text)

    lead = db.Column(db.Integer)

    handler = db.Column(db.String(50))

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    department = db.Column(db.String(50))

    alive = db.Column(db.Integer)

    missed = db.Column(db.String(10))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Lead(db.Model):
    __tablename__ = 'telle_lead'

    id = db.Column(db.Integer, primary_key=True)

    dealer_id = db.Column(db.String(100))
    customer_name = db.Column(db.String(80), nullable=True)

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    session_id = db.Column(db.String(120))

    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    notes_offer = db.Column(db.Text)

    appointment = db.Column(db.DateTime)

    department = db.Column(db.String(50))

    handler = db.Column(db.String(50))

    priority = db.Column(db.Integer)

    status = db.Column(db.String(20))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Lead %r>' % self.id


class Group(db.Model):
    __tablename__ = 'telle_group'

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.String(120), nullable=False)

    alive = db.Column(db.Integer, default=0)

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    department = db.Column(db.String(50))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Group %r>' % self.session_id
