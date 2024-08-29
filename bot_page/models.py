import datetime
from database.db_instance import db


class VautoCar(db.Model):
    __tablename__ = 'telle_inventory_vauto'

    # id = db.Column(db.Integer, primary_key=True)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    vin = db.Column(db.String(50), primary_key=True)
    stock = db.Column(db.String(50))

    new_used = db.Column(db.String(10))
    year = db.Column(db.Integer)

    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    model_number = db.Column(db.String(100))

    body = db.Column(db.Text)
    transmission = db.Column(db.Text)

    series = db.Column(db.String(50))

    body_door_ct = db.Column(db.Integer)
    odometer = db.Column(db.Integer)
    engine_cylinder_ct = db.Column(db.Integer)
    engine_displacement = db.Column(db.Float)
    drivetrain_desc = db.Column(db.String(20))
    colour = db.Column(db.Text)
    interior_color = db.Column(db.Text)
    msrp = db.Column(db.Float)
    price = db.Column(db.Float)
    inventory_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    certified = db.Column(db.String(10))
    description = db.Column(db.Text)

    features = db.Column(db.Text)

    photo_url_list = db.Column(db.Text)
    city_mpg = db.Column(db.Float)
    highway_mpg = db.Column(db.Float)

    photos_last_modified_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    series_detail = db.Column(db.Text)

    engine = db.Column(db.Text)

    fuel = db.Column(db.String(100))

    age = db.Column(db.Integer)

    bot_id = db.Column(db.String(100))

    def __repr__(self):
        return '<Car %r>' % self.vin


class HomenetCar(db.Model):
    __tablename__ = 'telle_inventory_homenet'

    # id = db.Column(db.Integer, primary_key=True)

    new_used = db.Column(db.String(50))

    stock = db.Column(db.String(50))
    vin = db.Column(db.String(50), primary_key=True)

    year = db.Column(db.Integer)

    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    body = db.Column(db.Text)
    series = db.Column(db.Text)
    model_number = db.Column(db.String(100))

    body_door_ct = db.Column(db.Integer)
    colour = db.Column(db.Text)
    interior_color = db.Column(db.Text)
    engine_cylinder_ct = db.Column(db.Integer)
    engine_displacement = db.Column(db.String(100))

    transmission = db.Column(db.Text)
    odometer = db.Column(db.Integer)

    price = db.Column(db.Integer)
    msrp = db.Column(db.Integer)
    bookvalue = db.Column(db.Integer)
    invoice = db.Column(db.Integer)

    certified = db.Column(db.Boolean)

    inventory_date = db.Column(db.Text)
    description = db.Column(db.Text)
    features = db.Column(db.Text)

    categorized_options = db.Column(db.Text)

    dealer_name = db.Column(db.Text)
    dealer_address = db.Column(db.Text)
    dealer_city = db.Column(db.String(50))
    dealer_state = db.Column(db.String(20))
    dealer_zip = db.Column(db.Integer)
    dealer_phone = db.Column(db.String(50))
    dealer_fax = db.Column(db.String(50))
    dealer_email = db.Column(db.String(50))

    comment_1 = db.Column(db.Text)
    comment_2 = db.Column(db.Text)
    comment_3 = db.Column(db.Text)
    comment_4 = db.Column(db.Text)
    comment_5 = db.Column(db.Text)

    style_description = db.Column(db.Text)
    ext_color_generic = db.Column(db.Text)
    ext_color_code = db.Column(db.Text)
    int_color_generic = db.Column(db.Text)
    int_color_code = db.Column(db.Text)

    int_upholstery = db.Column(db.Text)

    engine_block_type = db.Column(db.Text)
    engine_aspiration_type = db.Column(db.Text)
    engine = db.Column(db.Text)
    transmission_speed = db.Column(db.Float)
    transmission_description = db.Column(db.Text)

    drivetrain_desc = db.Column(db.Text)
    fuel = db.Column(db.Text)

    city_mpg = db.Column(db.Float)
    highway_mpg = db.Column(db.Float)

    epaclassification = db.Column(db.Text)
    wheelbase_code = db.Column(db.Float)

    internet_price = db.Column(db.Integer)
    misc_price1 = db.Column(db.Integer)
    misc_price2 = db.Column(db.Integer)
    misc_price3 = db.Column(db.Integer)

    factory_codes = db.Column(db.Text)
    marketclass = db.Column(db.Text)
    passengercapacity = db.Column(db.Integer)
    extcolorhexcode = db.Column(db.Text)

    intcolorhexcode = db.Column(db.Float)
    enginedisplacementcubicinches = db.Column(db.Float)

    photo_url_list = db.Column(db.Text)

    bot_id = db.Column(db.String(100))

    vdp_link = db.Column(db.Text)

    def __repr__(self):
        return '<HomenetCar %r>' % self.vin


class TodoModel(db.Model):
    __tablename__ = 'telle_todo'

    id = db.Column(db.Integer, primary_key=True)

    item = db.Column(db.Text)

    status = db.Column(db.Integer)

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class WebUserModel(db.Model):

    __tablename__ = 'telle_webuser'

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.String(120), nullable=False)

    ip_addr = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))

    device_type = db.Column(db.String(80))
    device_detail = db.Column(db.String(80))

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class WebUserPageView(db.Model):

    __tablename__ = 'telle_pageview'

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.String(120), nullable=False)
    ip_addr = db.Column(db.String(100))

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    bot_clicked = db.Column(db.Integer, default=0)

    page = db.Column(db.Text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Promotion(db.Model):
    __tablename__ = 'telle_promotion'

    id = db.Column(db.Integer, primary_key=True)

    promotion_name = db.Column(db.String(255), nullable=True)

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    code = db.Column(db.String(100))
    coupon = db.Column(db.Text)
    keywords = db.Column(db.Text)
    valid = db.Column(db.Integer, default=0)
    note = db.Column(db.Text)

    department = db.Column(db.String(50))

    deleted = db.Column(db.Integer, default=0)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class BotConfiguration(db.Model):

    __tablename__ = 'telle_bot_configure'

    id = db.Column(db.Integer, primary_key=True)

    bot_id = db.Column(db.String(100), unique=True)
    dealer_id = db.Column(db.String(100))

    dealer_bot_name = db.Column(db.Text)
    support_image = db.Column(db.Text)
    bot_init_text = db.Column(db.Text)
    bot_init_suggestions = db.Column(db.Text)

    dealer_chat_window_title = db.Column(db.Text)
    dealer_title_image = db.Column(db.Text)

    dealer_name = db.Column(db.Text)
    dealer_address = db.Column(db.Text)
    phone_numbers = db.Column(db.Text)
    sales_hours = db.Column(db.Text)
    service_hours = db.Column(db.Text)
    parts_hours = db.Column(db.Text)

    map_name = db.Column(db.Text)
    dealer_latitude = db.Column(db.Float)
    dealer_longitude = db.Column(db.Float)

    admin_name = db.Column(db.Text)

    published = db.Column(db.Integer, default=0)

    @classmethod
    def find_by_bot_id(cls, bot_id):
        return cls.query.filter_by(bot_id=bot_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
