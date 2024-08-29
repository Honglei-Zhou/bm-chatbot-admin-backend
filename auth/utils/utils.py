import ipinfo
from server.config import ipinfo_access_token
from bot_page.models import WebUserModel, WebUserPageView
from datetime import datetime


def update_user(message):
    try:
        device_type = message.get('deviceType', 'Desktop')
        device_detail = message.get('deviceDetail', 'Desktop')
        session_id = message.get('sessionId', '')

        dealer_id = message.get('dealerId', '2019123456001')
        dealer_name = message.get('dealerName', 'telle')

        ip_addr = message.get('ip_addr', '127.0.0.1')

        ip_details = get_ip_address(ip_addr)
        city = ip_details.get('city', 'NA')
        state = ip_details.get('region', 'NA')

        new_user = WebUserModel(dealer_id=dealer_id,
                                dealer_name=dealer_name,
                                device_detail=device_detail,
                                device_type=device_type,
                                created=datetime.utcnow(),
                                ip_addr=ip_addr,
                                city=city,
                                state=state,
                                session_id=session_id)

        new_user.save_to_db()

        return {
            'isError': False,
            'message': 'user: {} has been added'.format(ip_addr),
            'statusCode': 200,
            'data': ip_details
        }, 200
    except:
        return {
                   'isError': True,
                   'message': 'Internal Error',
                   'statusCode': 500,
               }, 500


def update_user_pageview(message):
    try:
        session_id = message.get('sessionId', '')

        dealer_id = message.get('dealerId', '2019123456001')

        ip_addr = message.get('ip_addr', '127.0.0.1')

        page = message.get('page', ''),
        bot_clicked = message.get('bot_clicked')

        new_pageview = WebUserPageView(
                                dealer_id=dealer_id,
                                created=datetime.utcnow(),
                                ip_addr=ip_addr,
                                page=page,
                                bot_clicked=bot_clicked,
                                session_id=session_id)

        new_pageview.save_to_db()

        return {
            'isError': False,
            'message': 'user page view: {} has been added'.format(ip_addr),
            'statusCode': 200,
            'data': page
        }, 200
    except:
        return {
                   'isError': True,
                   'message': 'Internal Error',
                   'statusCode': 500,
               }, 500


def get_ip_address(ip):
    handler = ipinfo.getHandler(ipinfo_access_token)
    details = handler.getDetails(ip)
    return details.all


def get_random_pwd(string_length=6):
    import random
    import string
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(string_length))

