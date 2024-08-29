from chatbot.models import Message, Chat, Lead, Group
from chatbot.fields import *
from common.utils import *
import datetime
import json
from sqlalchemy import and_, desc, text
from database.db_instance import db


from_user_map = {'bot': 'BM Bot', 'customer': 'User', 'admin': 'Admin'}
imgUrl_map = {'bot': 'support', 'customer': 'user', 'admin': 'me'}


def get_messages(page=1, page_size=20, direction='', sort='+id', session_id='', dealer_id=None, start_time=None, end_time=None):
    if dealer_id is None:
        return {'count': 0, 'total': 0, 'has_next': False, 'data': []}
    if start_time is None:
        start_time = datetime.datetime.utcnow() - datetime.timedelta(days=3650)
    if end_time is None:
        end_time = datetime.datetime.utcnow()

    query_time = datetime.datetime(2019, 5, 1)

    if sort == '-id':
        items = Message.query.filter(and_(Message.direction.ilike('%{}%'.format(direction)),
                                          Message.dealer_id.ilike('%{}%'.format(dealer_id)),
                                          Message.session_id.ilike('%{}%'.format(session_id)),
                                          Message.created_time >= query_time)).order_by(desc(Message.id)).all()
    else:
        items = Message.query.filter(and_(Message.direction.ilike('%{}%'.format(direction)),
                                          Message.dealer_id.ilike('%{}%'.format(dealer_id)),
                                          Message.session_id.ilike('%{}%'.format(session_id)),
                                          Message.created_time >= query_time)).order_by(Message.id).all()

    total = len(items)
    has_next = False

    messages = []

    for item in items:
        # message_data = json.loads(item.message)
        data = {
            'id': item.id,
            'customer_name': item.customer_name,
            'session_id': item.session_id,
            'direction': item.direction,
            'message': item.message,
            'created_time': item.created_time,
            'from_bot': item.from_bot,
            'from_user': item.message_owner,
            'is_read': item.is_read
        }
        # print(item.created_time)
        messages.append(data)
    return marshal_list_data(messages,
                             has_next=has_next,
                             total=total,
                             list_fields=message_list_fields,
                             detail_fields=message_meta_fields)


def get_full_message(message_id):
    message = Message.query.filter_by(id=message_id).first()

    if message is None:

        return False, {
                        'isError': True,
                        'message': 'message {} does not exist.'.format(message_id),
                        'statusCode': 200,
                        'data': None
                        }

    return marshal_message(message)


def marshal_message(message):
    message_data = json.loads(message.message)

    data = {
        'id': message.id,
        'customer_name': message.customer_name,
        'session_id': message.session_id,
        'direction': message.direction,
        'message': message_data,
        'created_time': message.created_time.timestamp()
    }

    return data


def get_chat_sessions(page=1, page_size=20, department='', missed='', handler='', dealer_id=None, start_time=None, end_time=None):
    if dealer_id is None:
        return {'count': 0, 'total': 0, 'has_next': False, 'data': []}
    if start_time is None:
        start_time = datetime.datetime.utcnow() - datetime.timedelta(days=3650)
    if end_time is None:
        end_time = datetime.datetime.utcnow()

    query_time = datetime.datetime(2019, 5, 1)

    items = Chat.query.filter(and_(Chat.department.ilike('%{}%'.format(department)),
                                   Chat.dealer_id.ilike('%{}%'.format(dealer_id)),
                                   Chat.missed.ilike('%{}%'.format(missed)),
                                   Chat.started >= query_time,
                                   Chat.handler.ilike('%{}%'.format(handler)))).order_by(desc(Chat.id)).all()

    total = len(items)
    has_next = False

    return marshal_list_data(items,
                             has_next=has_next,
                             total=total,
                             list_fields=chat_list_fields,
                             detail_fields=chat_meta_fields)


def get_full_chat_session(session_id):
    messages = Message.query.filter_by(session_id=session_id).order_by(Message.created_time).all()

    chat = Chat.query.filter_by(session_id=session_id).first()

    if chat is None:
        return False, {
            'isError': True,
            'message': 'Chat {} does not exist.'.format(session_id),
            'statusCode': 200,
            'data': None
        }

    chat_data = []

    for message in messages:
        chat_data.append(marshal_message(message))

    data = {
        'id': chat.id,
        'customer_name': chat.customer_name,
        'session_id': chat.session_id,

        'device_type': chat.device_type,
        'device_detail': chat.device_detail,
        'started': chat.started,
        'duration': chat.duration,
        'lead': chat.lead,
        'handler': chat.handler,
        'dealer_id': chat.dealer_id,
        'dealer_name': chat.dealer_name,
        'department': chat.department,
        'missed': chat.missed,
        'messages': chat_data
    }

    return data


def get_leads(page=1,
              page_size=20,
              department='',
              handler='',
              notes_offer='',
              customer_name='',
              sort='-id',
              priority=1
              ):

    if sort == '-id':
        pagination = Lead.query.\
            filter(Lead.department.ilike('%{}%'.format(department))
                   & (Lead.status.ilike('%New%') | Lead.status.ilike('%Closed%') | Lead.status.ilike('%Success%'))
                   & Lead.handler.ilike('%{}%'.format(handler))
                   & Lead.customer_name.ilike('%{}%'.format(customer_name))
                   & Lead.notes_offer.ilike('%{}%'.format(notes_offer))
                   & (Lead.priority >= priority)).order_by(desc(Lead.id)).paginate(page=page, per_page=page_size)
    else:
        pagination = Lead.query. \
            filter(Lead.department.ilike('%{}%'.format(department))
                   & (Lead.status.ilike('%New%') | Lead.status.ilike('%Closed%') | Lead.status.ilike('%Success%'))
                   & Lead.handler.ilike('%{}%'.format(handler))
                   & Lead.customer_name.ilike('%{}%'.format(customer_name))
                   & Lead.notes_offer.ilike('%{}%'.format(notes_offer))
                   & (Lead.priority >= priority)).order_by(Lead.id).paginate(page=page, per_page=page_size)
    items = pagination.items

    total = pagination.total
    has_next = pagination.has_next

    return marshal_list_data(items,
                             has_next=has_next,
                             total=total,
                             list_fields=lead_list_fields,
                             detail_fields=lead_meta_fields)


def get_leads_v2(dealer_id, handler='', sort='-id'):
    query_time = datetime.datetime(2019, 5, 1)

    if sort == '-id':
        items = Lead.query.filter(and_(Lead.dealer_id == dealer_id, Lead.handler.ilike('%{}%'.format(handler)), Lead.created >= query_time)).order_by(desc(Lead.id)).all()
    else:
        items = Lead.query. \
            filter(and_(Lead.dealer_id == dealer_id, Lead.handler.ilike('%{}%'.format(handler)), Lead.created >= query_time)).order_by(Lead.id).all()

    total = len(items)
    has_next = False

    return marshal_list_data(items,
                             has_next=has_next,
                             total=total,
                             list_fields=lead_list_fields,
                             detail_fields=lead_meta_fields)


def get_full_lead(dealer_id, id):
    lead = Lead.query.filter_by(dealer_id=dealer_id, id=id).first()

    # print(lead)

    if lead is None:
        return False, {
            'isError': True,
            'message': 'Lead {} does not exist.'.format(id),
            'statusCode': 200,
            'data': None
        }

    return marshal_list_data([lead],
                             has_next=False,
                             total=1,
                             list_fields=lead_list_fields,
                             detail_fields=lead_meta_fields)


def get_live_messages(session_id, page=1, page_size=40):

    items = Message.query.filter(Message.session_id.ilike('%{}%'.format(session_id))).order_by(Message.id).all()

    total = len(items)
    has_next = False

    messages = []

    for item in items:
        data = {
            'id': item.id,
            'from_bot': item.from_bot,
            'session_id': item.session_id,
            'direction': item.direction,
            'message': item.message,
            'created': item.created_time,
            'is_read': item.is_read,
        }

        messages.append(data)
    return marshal_list_data(messages,
                             has_next=has_next,
                             total=total,
                             list_fields=live_message_list_fields,
                             detail_fields=live_message_meta_fields)


def get_live_chats(dealer_id):

    items = Message.query.join(Group, Group.session_id == Message.session_id).filter(Group.alive == 1, Group.dealer_id.ilike('%{}%'.format(dealer_id))).order_by(desc(Message.id)).all()

    total = len(items)
    has_next = False

    messages = {}

    for item in items:
        # print(type(item.is_read))
        session_id = item.session_id
        if session_id in messages:
            if item.is_read == 0:
                messages[session_id]['un_read'] += 1
        else:
            if item.is_read == 0:
                unread = 1
            else:
                unread = 0
            messages[session_id] = {
                'id': item.id,
                'from_bot': item.from_bot,
                'session_id': item.session_id,
                'direction': item.direction,
                'message': item.message,
                'created': item.created_time,
                'imgUrl': imgUrl_map[item.message_owner.strip()],
                'un_read': unread,
                'from_user': from_user_map[item.message_owner.strip()]
            }

    messages = [value for key, value in messages.items()]
    return marshal_list_data(messages,
                             has_next=has_next,
                             total=total,
                             list_fields=live_chat_list_fields,
                             detail_fields=live_chat_meta_fields)


def update_live_message(session_id=''):
    if session_id == '':
        return {
            'isError': False,
            'message': 'Update Successfully.',
            'statusCode': 200,
            'data': None}
    db.session.execute('update telle_message set is_read = 1 where session_id ilike :session', {'session': '%{}%'.format(session_id)})

    db.session.commit()
    return {
            'isError': False,
            'message': 'Update Successfully.',
            'statusCode': 200,
            'data': None}


def update_chat(session_id=''):
    if session_id == '':
        return {
            'isError': False,
            'message': 'Update Successfully.',
            'statusCode': 200,
            'data': None}

    db.session.execute('update telle_group set alive = 0 where session_id ilike :session',
                       {'session': '%{}%'.format(session_id)})

    db.session.commit()
    return {
        'isError': False,
        'message': 'Update Successfully.',
        'statusCode': 200,
        'data': None}
