from database.db_instance import db
from passlib.hash import pbkdf2_sha256 as sha256
import datetime


class BotAuth(db.Model):
    __tablename__ = 'telle_bot_auth'

    id = db.Column(db.Integer, primary_key=True)

    bot_id = db.Column(db.String(100))
    origin = db.Column(db.String(255))
    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)
    dealer_address = db.Column(db.Text)
    dealer_latitude = db.Column(db.Float)
    dealer_longitude = db.Column(db.Float)

    dealer_default_image = db.Column(db.Text)

    dealer_info = db.Column(db.Text)

    dealer_bot_name = db.Column(db.Text)

    bot_init_text = db.Column(db.Text)
    bot_init_suggestions = db.Column(db.Text)

    support_name = db.Column(db.String(50))
    admin_name = db.Column(db.Text)

    service_link = db.Column(db.Text)
    service_phone_number = db.Column(db.String(50))

    phone_numbers = db.Column(db.Text)
    sales_hours = db.Column(db.Text)
    service_hours = db.Column(db.Text)
    parts_hours = db.Column(db.Text)

    dealer_chat_window_title = db.Column(db.Text)
    dealer_title_image = db.Column(db.Text)
    dealer_image_prefix = db.Column(db.Text)
    support_image = db.Column(db.Text)
    admin_image = db.Column(db.Text)

    permission = db.Column(db.String(100), default='trial')

    @staticmethod
    def generate_hash(origin):
        return sha256.hash(origin)

    @staticmethod
    def verify_hash(origin, hash):
        return sha256.verify(origin, hash)

    @classmethod
    def find_by_bot_id(cls, bot_id):
        return cls.query.filter_by(bot_id=bot_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


# roles_users = db.Table('cars_dthonda_roles_users',
#         db.Column('user_id', db.Integer(), db.ForeignKey('cars_dthonda_user.id')),
#         db.Column('role_id', db.Integer(), db.ForeignKey('cars_dthonda_role.id')))

class Department(db.Model):
    __tablename__ = 'telle_department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Role(db.Model):
    __tablename__ = 'telle_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = 'telle_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # User/Admin
    roles = db.Column(db.String(80))

    # Sales/Service/Management
    departments = db.Column(db.String(80))

    avatar = db.Column(db.Text)
    introduction = db.Column(db.Text)

    dealer_id = db.Column(db.String(100))

    dealer_url = db.Column(db.Text)

    # Custom User Payload
    def get_security_payload(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'roles': self.roles,
            'departments': self.departments,
            'created': self.created,
            'avatar': self.avatar,
            'introduction': self.introduction,
            'dealer_id': self.dealer_id
        }

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def delete(cls, email):
        try:
            user = cls.query.filter_by(email=email).first()
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User: {} is deleted.'.format(email)}
        except:
            return {'message': 'Something went wrong'}


class RevokedTokenModel(db.Model):

    __tablename__ = 'telle_revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class IPModel(db.Model):

    __tablename__ = 'telle_visitors_ip'

    id = db.Column(db.Integer, primary_key=True)
    ip_addr = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    bot_id = db.Column(db.String(255))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class BotBackendResponse(db.Model):
    __tablename__ = 'telle_bot_response'

    id = db.Column(db.Integer, primary_key=True)

    bot_id = db.Column(db.String(100))
    dealer_id = db.Column(db.String(100))

    init_info = db.Column(db.Text)

    init_new = db.Column(db.Text)
    init_used = db.Column(db.Text)
    init_service = db.Column(db.Text)

    testdrive_info = db.Column(db.Text)

    @classmethod
    def find_by_bot_id(cls, bot_id):
        return cls.query.filter_by(bot_id=bot_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
