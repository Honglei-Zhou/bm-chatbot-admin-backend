from bot_page.models import *
from flask_restful import marshal
from bot_page.fields import *
from database.db_instance import db
from sqlalchemy import text, desc


def marshal_list_data(items, has_next=False, total=0, delimiter='|'):
    data = {'count': 0, 'total': 0, 'has_next': has_next, 'data': []}
    for car in items:
        if car.photo_url_list is None:
            car.photo_url_list = []
        else:
            car.photo_url_list = car.photo_url_list.split(delimiter)

        if hasattr(car, 'vdp_link'):
            car.link = car.vdp_link
        else:
            car.link = ''
        item = marshal(car, car_fields)
        data['data'].append(item)
        data['count'] += 1
    data['total'] = total

    return marshal(data, car_list_fields)


def marshal_list_detail_data(items, delimiter='|'):
    data = {'count': 0, 'has_next': False, 'data': []}
    for car in items:
        if car.features is None:
            car.features = []
        else:
            car.features = car.features.split(delimiter)
        if car.photo_url_list is None:
            car.photo_url_list = []
        else:
            car.photo_url_list = car.photo_url_list.split(delimiter)

        item = marshal(car, car_detail_fields)
        data['data'].append(item)
        data['count'] += 1

    return marshal(data, car_list_detail_fields)


def get_all_cars(dealer_id=None, page=1, page_size=20):
    if dealer_id and ('2019789' in dealer_id or '201912345600' in dealer_id):
        Car = VautoCar
        delimiter = '|'
    elif dealer_id and '2019791' in dealer_id:
        Car = HomenetCar
        delimiter = ','
    else:
        return marshal_list_data([], has_next=False, total=0)

    items = Car.query.filter_by(bot_id=dealer_id).order_by(-Car.year).all()

    total = len(items)
    has_next = False

    return marshal_list_data(items, has_next=has_next, total=total, delimiter=delimiter)


def get_new_cars(dealer_id=None, page=1, page_size=20):

    if dealer_id and ('2019789' in dealer_id or '201912345600' in dealer_id):
        Car = VautoCar
        new_used = 'N'
        delimiter = '|'
    elif dealer_id and '2019791' in dealer_id:
        Car = HomenetCar
        new_used = 'New'
        delimiter = ','
    else:
        return marshal_list_data([], has_next=False, total=0)

    pagination = Car.query.filter_by(new_used=new_used, bot_id=dealer_id).order_by(-Car.year).paginate(page=page, per_page=page_size)
    cars = pagination.items
    total = pagination.total
    has_next = pagination.has_next

    return marshal_list_data(cars, has_next=has_next, total=total, delimiter=delimiter)


def get_used_cars(dealer_id=None, page=1, page_size=20):
    if dealer_id and ('2019789' in dealer_id or '201912345600' in dealer_id):
        Car = VautoCar
        new_used = 'U'
        delimiter = '|'
    elif dealer_id and '2019791' in dealer_id:
        Car = HomenetCar
        new_used = 'Used'
        delimiter = ','
    else:
        return marshal_list_data([], has_next=False, total=0)

    pagination = Car.query.filter_by(new_used=new_used, bot_id=dealer_id).order_by(-Car.year).paginate(page=page, per_page=page_size)
    cars = pagination.items
    total = pagination.total
    has_next = pagination.has_next

    return marshal_list_data(cars, has_next=has_next, total=total, delimiter=delimiter)


def get_car_by_vin(vin, dealer_id=None):
    if dealer_id and ('2019789' in dealer_id or '201912345600' in dealer_id):
        Car = VautoCar
    elif dealer_id and '2019791' in dealer_id:
        Car = HomenetCar
    else:
        return marshal_list_detail_data([])
    
    cars = Car.query.filter_by(vin=vin, bot_id=dealer_id).all()

    return marshal_list_detail_data(cars)


def marshal_line_chart(newVisits, newMessages, chatSessions):

    visits = {
        'name': 'New Visits',
        'data': [],
        'x_axis': [],
        'legend': 'Total New Visits'
    }
    visits_count = 0
    for new_visit in newVisits:
        visits_count += 1
        visits['data'].append(new_visit.counted_visits)
        visits['x_axis'].append(new_visit.count_date)

    marshaled_visits = marshal(visits, new_visits_fields)

    messages = {
        'name': 'New Messages',
        'data': [],
        'x_axis': [],
        'legend': 'Total Messages'
    }

    message_count = 0
    for new_message in newMessages:
        message_count += 1
        messages['data'].append(new_message.counted_messages)
        messages['x_axis'].append(new_message.count_date)

    marshaled_messages = marshal(messages, messages_fields)

    chat_sessions = {
        'name': 'New Chat Sessions',
        'data': [],
        'x_axis': [],
        'legend': 'Total Chat Sessions'
    }

    chat_count = 0
    for new_chat in chatSessions:
        chat_count += 1
        chat_sessions['data'].append(new_chat.counted_chats)
        chat_sessions['x_axis'].append(new_chat.count_date)

    marshaled_sessions = marshal(chat_sessions, chat_sessions_fields)

    chart_data = {
        'newVisits': marshaled_visits,
        'messages': marshaled_messages,
        'chatSessions': marshaled_sessions
    }

    return marshal(chart_data, line_chart_fields)


def marshal_line_chart_adv(newVisits, newMessages, chatSessions):

    visits = {
        'name': 'New Visits',
        'date': [],
        'city': [],
        'legend': 'Total New Visits'
    }
    for new_visit in newVisits:
        visits['date'].append(new_visit.created)
        visits['city'].append(new_visit.city)

    marshaled_visits = marshal(visits, new_visits_list_fields)

    messages = {
        'name': 'New Messages',
        'date': [],
        'direction': [],
        'legend': 'Total Messages'
    }

    for new_message in newMessages:
        messages['date'].append(new_message.created_time)
        messages['direction'].append(new_message.direction)

    marshaled_messages = marshal(messages, messages_list_fields)

    chat_sessions = {
        'name': 'New Chat Sessions',
        'date': [],
        'legend': 'Total Chat Sessions'
    }

    for new_chat in chatSessions:
        chat_sessions['date'].append(new_chat.started)

    marshaled_sessions = marshal(chat_sessions, chat_sessions_list_fields)

    chart_data = {
        'newVisits': marshaled_visits,
        'messages': marshaled_messages,
        'chatSessions': marshaled_sessions
    }
    return marshal(chart_data, line_chart_fields_adv)


def get_line_chart():
    current_time = datetime.datetime.utcnow()

    five_days_ago = current_time - datetime.timedelta(days=5)

    new_visits_sql = text('select count(date(created)) as counted_visits, date(created) as count_date '
                          'from telle_webuser where created > :val group by date(created) order by date(created)')

    # new_visits_sql = text('select count(date(created_time)) as counted_visits, date(created_time) as count_date '
    #                     'from cars_dthonda_message where created_time > :val group by date(created_time) order by date(created_time)')

    newVisits = db.engine.execute(new_visits_sql, {'val': five_days_ago})

    messages_sql = text('select count(date(created_time)) as counted_messages, date(created_time) as count_date '
                        'from telle_message where created_time > :val group by date(created_time) order by date(created_time)')
    messages = db.engine.execute(messages_sql, {'val': five_days_ago})

    chat_sessions_sql = text('select count(date(started)) as counted_chats, date(started) as count_date '
                             'from telle_chat where started > :val group by date(started) order by date(started)')

    # chat_sessions_sql = text('select count(date(created_time)) as counted_chats, date(created_time) as count_date '
    #                       'from cars_dthonda_message where created_time > :val group by date(created_time) order by date(created_time)')
    chatSessions = db.engine.execute(chat_sessions_sql, {'val': five_days_ago})

    return marshal_line_chart(newVisits, messages, chatSessions)


def get_line_chart_adv(start, end):
    new_visits_sql = text('select created as created, city as city '
                          'from telle_webuser where created >= :start and created <= :end order by date(created)')

    newVisits = db.engine.execute(new_visits_sql, {'start': start, 'end': end})

    messages_sql = text('select created_time as created_time, direction as direction '
                        'from telle_message where created_time >= :start and created_time <= :end order by date(created_time)')
    messages = db.engine.execute(messages_sql, {'start': start, 'end': end})

    chat_sessions_sql = text('select started as started '
                             'from telle_chat where started >= :start and started <= :end order by date(started)')

    chatSessions = db.engine.execute(chat_sessions_sql, {'start': start, 'end': end})

    return marshal_line_chart_adv(newVisits, messages, chatSessions)


def get_line_chart_v3(start, dealer_id):
    new_visits_sql = text('select count(date(created)) as counted_visits, date(created) as count_date '
                          'from telle_webuser where dealer_id = :dealer_id and created > :val group by date(created) order by date(created)')

    newVisits = db.engine.execute(new_visits_sql, {'dealer_id': dealer_id, 'val': start})

    messages_sql = text('select count(date(created_time)) as counted_messages, date(created_time) as count_date '
                        'from telle_message where dealer_id = :dealer_id and created_time > :val group by date(created_time) order by date(created_time)')
    messages = db.engine.execute(messages_sql, {'dealer_id': dealer_id, 'val': start})

    chat_sessions_sql = text('select count(date(started)) as counted_chats, date(started) as count_date '
                             'from telle_chat where dealer_id = :dealer_id and started > :val group by date(started) order by date(started)')

    chatSessions = db.engine.execute(chat_sessions_sql, {'dealer_id': dealer_id, 'val': start})

    return marshal_line_chart(newVisits, messages, chatSessions)


def marshal_pie_chart(data):
    pie_data = []
    for d in data:
        item = {'value': d.counted_visits, 'name': d.count_city}
        pie_data.append(marshal(item, pie_chart_value_fields))

    return marshal({'data': pie_data}, pie_chart_fields)


def marshal_pie_chart_v2(data):
    pie_data = []
    for d in data:
        item = {'date': d.created, 'value': d.counted_visits, 'name': d.count_city}
        pie_data.append(marshal(item, pie_chart_value_fields_v2))

    return marshal({'data': pie_data}, pie_chart_fields_v2)


def get_pie_chart():
    current_time = datetime.datetime.utcnow()

    five_days_ago = current_time - datetime.timedelta(days=5)

    new_visits_sql = text('select count(city) as counted_visits, city as count_city '
                          'from telle_webuser where created > :val group by city order by city')

    newVisits = db.engine.execute(new_visits_sql, {'val': five_days_ago})

    return marshal_pie_chart(newVisits)


def get_pie_chart_v2(start, dealer_id):

    new_visits_sql = text('select count(city) as counted_visits, date(created) as created, city as count_city '
                          'from telle_webuser where dealer_id = :dealer_id and created > :val group by city, date(created) order by date(created)')

    newVisits = db.engine.execute(new_visits_sql, {'dealer_id': dealer_id, 'val': start})

    return marshal_pie_chart_v2(newVisits)


def marshal_bar_chart(newVisits):
    bar_chart = {'Morning': {}, 'Afternoon': {}, 'Evening': {}}
    count = 0
    for d in newVisits:
        count += 1
        key = str(d.day)
        if key not in bar_chart['Morning']:
            bar_chart['Morning'][key] = 0
            bar_chart['Afternoon'][key] = 0
            bar_chart['Evening'][key] = 0
        if 6 <= d.hour <= 12:
            bar_chart['Morning'][key] += d.hourly_visits
        elif 12 < d.hour <= 18:
            bar_chart['Afternoon'][key] += d.hourly_visits
        else:
            bar_chart['Evening'][key] += d.hourly_visits

    if count == 0:
        return {'name': 'Time', 'data': [], 'x_axis': None}
    marshal_data = []
    axis = []
    for key, value in bar_chart.items():
        axis = [k for k, v in value.items()]

        marshal_data.append(marshal({'name': key, 'data': [v for k, v in value.items()], 'legend': key},
                        bar_chart_value_fields))

    return marshal({'name': 'Time', 'data': marshal_data, 'x_axis': axis}, bar_chart_fields)


def get_bar_chart():
    current_time = datetime.datetime.utcnow()

    five_days_ago = current_time - datetime.timedelta(days=360)

    new_visits_sql = text("select count(*) as hourly_visits, foo.hour, foo.day from "
                          "(select date_part('hour', timezone) as hour, date(timezone) as day "
                          "from (select created at time zone 'utc' at time zone 'america/chicago' from telle_webuser "
                          "where created > :val group by created order by date(created)) as par) as foo "
                          "group by foo.hour, foo.day order by foo.day")

    new_visits = db.engine.execute(new_visits_sql, {'val': five_days_ago})

    return marshal_bar_chart(new_visits)


def get_bar_chart_v2(start, dealer_id):

    new_visits_sql = text("select count(*) as hourly_visits, foo.hour, foo.day from "
                          "(select date_part('hour', timezone) as hour, date(timezone) as day "
                          "from (select created at time zone 'utc' at time zone 'america/chicago' from telle_webuser "
                          "where dealer_id = :dealer_id and created > :val group by created order by date(created)) as par) as foo "
                          "group by foo.hour, foo.day order by foo.day")

    new_visits = db.engine.execute(new_visits_sql, {'dealer_id': dealer_id, 'val': start})

    return marshal_bar_chart(new_visits)


def marshal_todo_list(todos):
    total = 0
    items = []
    for todo in todos:
        total += 1
        items.append(marshal({'id': todo.id, 'text': todo.item, 'done': todo.status == 1}, todo_fields))

    return marshal({'total': total, 'items': items}, todo_list_fields)


def get_todo_list():
    current_time = datetime.datetime.utcnow()

    five_days_ago = current_time - datetime.timedelta(days=5)

    todo_sql = text("select * from telle_todo where created > :val and status >= 0")

    todos = db.engine.execute(todo_sql, {'val': five_days_ago})

    return marshal_todo_list(todos)


def get_user_location(dealer_id='', session_id=''):
    if session_id == '':
        return {
            'isError': False,
            'message': 'Session id can not be empty',
            'statusCode': 200,
            'data': None}

    item = WebUserModel.query.filter(WebUserModel.session_id.ilike('%{}%'.format(session_id))).order_by(desc(WebUserModel.id)).first()

    user_location = {
        'session_id': session_id,
        'city': 'NA',
        'state': 'NA',
        'device_type': 'NA',
        'device_detail': 'NA'
    }
    print(item)
    if item:
        user_location['session_id'] = item.session_id
        user_location['city'] = item.city
        user_location['state'] = item.state
        user_location['device_type'] = item.device_type
        user_location['device_detail'] = item.device_detail

    return marshal(user_location, webuser_fields)


def marshal_promotion_list(promos):
    total = 0
    items = []
    for promo in promos:
        total += 1
        item = {
            'id': promo.id,
            'promotion_name': promo.promotion_name,
            'dealer_id': promo.dealer_id,
            'dealer_name': promo.dealer_name,
            'code': promo.code,
            'coupon': promo.coupon,
            'keywords': promo.keywords,
            'note': promo.note,
            'department': promo.department,
            'start_date': promo.start_date,
            'end_date': promo.end_date,
            'created': promo.created,
            'valid': promo.valid
        }
        items.append(marshal(item, promotion_fields))

    return marshal({'total': total, 'promotions': items}, promotion_list_fields)


def get_promotion_list(dealer_id):

    promotion_sql = text("select * from telle_promotion where dealer_id = :val and deleted = 0 order by -id")

    promos = db.engine.execute(promotion_sql, {'val': dealer_id})

    return marshal_promotion_list(promos)


def get_bot_configuration(bot_id):
    item = BotConfiguration.find_by_bot_id(bot_id)
    if item:
        return marshal(item, bot_configuration_fields)
    else:
        return {
            'isError': False,
            'message': 'No configuration found',
            'statusCode': 200,
            'data': None}
