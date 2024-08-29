from auth.models import User, BotAuth
from flask_restful import marshal
from auth.fields import *


def marshal_list_data(items, has_next=False, total=0):
    data = {'count': 0, 'total': total, 'has_next': has_next, 'data': []}
    for user in items:

        item = marshal(user, user_detail_fields)
        data['data'].append(item)
        data['count'] += 1
    data['total'] = total

    return marshal(data, user_list_fields)


def marshal_list_detail_data(item):
    data = {'count': 0, 'total': 1, 'has_next': False, 'data': []}

    user = marshal(item, user_detail_fields)
    data['data'].append(user)
    data['count'] += 1

    print(data)

    return marshal(data, user_list_fields)


def get_all_users(page=1, page_size=20):
    print(page)
    print(page_size)
    pagination = User.query.order_by(User.departments).paginate(page=page, per_page=page_size)
    users = pagination.items
    total = pagination.total
    has_next = pagination.has_next

    return marshal_list_data(users, has_next=has_next, total=total)


def get_user_detail(email, dealer_id):

    user = User.query.filter_by(email=email, dealer_id=dealer_id).first()
    print(user)
    if user:
        return marshal_list_detail_data(user)
    else:
        return {
                   'isError': True,
                   'message': 'Permission denied.',
                   'statusCode': 200,
                   'data': None
               }, 200


def get_all_users_by_dealer_id(dealer_id, page=1, page_size=20):
    pagination = User.query.filter_by(dealer_id=dealer_id).order_by(User.departments).paginate(page=page, per_page=page_size)
    users = pagination.items
    total = pagination.total
    has_next = pagination.has_next

    return marshal_list_data(users, has_next=has_next, total=total)


def marshal_bot_data(items, is_authorized=False):
    data = {
        'isError': False,
        'message': 'Success',
        'statusCode': 200,
        'isAuthorized': is_authorized
    }
    # print(items[0])
    items[0].isAuthorized = is_authorized

    item = marshal(items[0], bot_detail_fields)
    data['data'] = item

    return marshal(data, bot_fields)


def get_bot_by_dealer_id(dealer_id):

    bot = BotAuth.query.filter_by(bot_id=dealer_id).all()

    if len(bot) == 0 or len(bot) > 1 or bot[0].permission == 'expired':
        return {'isError': False,
                'message': 'Failed',
                'statusCode': 200,
                'isAuthorized': False,
                'data': {'isAuthorized': False}
                }, 200
    else:
        return marshal_bot_data(bot, is_authorized=True), 200

