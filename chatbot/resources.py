from flask_restful import Resource, reqparse
from flask_jwt_extended import \
    (create_access_token, create_refresh_token, jwt_required, get_jwt_claims,
     jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import request, jsonify
from chatbot.handler import (get_messages, get_full_message, get_chat_sessions, get_live_messages, get_live_chats,
                             get_full_chat_session, get_full_lead, get_leads, update_live_message, update_chat, get_leads_v2)
import datetime
from .models import Lead
from .utils.send_email import send_email
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

default_page_size = 20


class MessageList(Resource):

    @jwt_required
    def get(self):

        # GET Filter Fields
        # Support filter by: session_id, direction, start_time and end_time
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', default_page_size, type=int)
        session_id = request.args.get('sessionId', '').strip()
        direction = request.args.get('direction', '').strip()
        start_time = request.args.get('start_time', None)
        end_time = request.args.get('end_time', None)
        sort = request.args.get('sort', '+id')

        dealer_id = request.args.get('dealerId', None)

        print(session_id)

        roles = get_jwt_claims()['roles']

        if roles == 'admin':
            # Retrieve all user data
            return get_messages(page=page,
                                page_size=page_size,
                                session_id=session_id,
                                dealer_id=dealer_id,
                                direction=direction,
                                sort=sort,
                                start_time=start_time,
                                end_time=end_time), 200
        else:
            allowed_start_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)
            # message = ''
            if session_id == '':
                if start_time is None or start_time < allowed_start_time:
                    start_time = allowed_start_time
                    # message = 'You are only allowed to retrieve recent 5 days chat history.'
            # Non-admin can only view one page of messages
            return get_messages(page=1,
                                page_size=page_size,
                                session_id=session_id,
                                dealer_id=dealer_id,
                                direction=direction,
                                start_time=start_time,
                                end_time=end_time), 200


class LiveMessageList(Resource):

    @jwt_required
    def get(self):

        # session_id can not be empty here. TO LIST
        session_id = request.args.get('session_id', '').strip()

        return get_live_messages(session_id=session_id), 200


class LiveChatList(Resource):

    @jwt_required
    def get(self):
        dealer_id = request.args.get('dealerId', '').strip()
        print(dealer_id)
        # logger.info(request)
        return get_live_chats(dealer_id), 200


class LiveChatUpdate(Resource):

    @jwt_required
    def get(self):
        session_id = request.args.get('session_id', '').strip()
        return update_live_message(session_id=session_id), 200


class MessageDetail(Resource):
    @jwt_required
    def get(self, id):

        message = get_full_message(id)

        return message, 200


class ChatUpdate(Resource):

    @jwt_required
    def get(self):
        session_id = request.args.get('session_id', '').strip()
        return update_chat(session_id=session_id), 200


class ChatList(Resource):

    @jwt_required
    def get(self):

        # GET Filter Fields
        # Support filter by: department, missed, started
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', default_page_size, type=int)
        department = request.args.get('department', '').strip()
        missed = request.args.get('missed', '').strip()
        start_time = request.args.get('start_time', None)

        dealer_id = request.args.get('dealerId', None)

        departments = get_jwt_claims()['departments']

        email = ''

        if departments == 'management':
            # Retrieve all user data
            return get_chat_sessions(page=page,
                                     page_size=page_size,
                                     department=department,
                                     missed=missed,
                                     dealer_id=dealer_id,
                                     start_time=start_time,
                                     handler=email), 200
        else:
            allowed_start_time = datetime.datetime.utcnow() - datetime.timedelta(days=5)

            if start_time is None or start_time < allowed_start_time:
                start_time = allowed_start_time

            # Non management department can only view chats from his/her department
            return get_chat_sessions(page=page,
                                     page_size=page_size,
                                     department=departments,
                                     missed=missed,
                                     dealer_id=dealer_id,
                                     start_time=start_time,
                                     handler=email), 200


class ChatDetail(Resource):
    @jwt_required
    def get(self, session_id):

        chat = get_full_chat_session(session_id)

        return chat, 200


class LeadListV2(Resource):
    @jwt_required
    def get(self):
        print('In Getting')
        # GET Filter Fields
        # Support filter by: department, missed, started
        dealer_id = request.args.get('dealerId', '2019123456001')
        sort = request.args.get('sort', '-id')

        roles = get_jwt_claims()['roles']
        departments = get_jwt_claims()['departments']
        email = get_jwt_identity()

        if departments == 'management':
            # Retrieve all user data
            return get_leads_v2(dealer_id, sort=sort), 200
        else:
            # Non admin user can only view user's own leads.
            if email == '':
                return {
                           'isError': True,
                           'message': 'Permission denied.',
                           'statusCode': 200,
                           'data': None
                       }, 200
            else:
                return get_leads_v2(dealer_id, sort=sort, handler=email), 200


class LeadList(Resource):

    @jwt_required
    def get(self):
        print('In Getting')
        # GET Filter Fields
        # Support filter by: department, missed, started
        dealer_id = request.args.get('dealerId', '2019123456001')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('limit', default_page_size, type=int)
        department = request.args.get('department', '').strip()
        priority = request.args.get('importance', 1)
        sort = request.args.get('sort', '-id')
        notes_offer = request.args.get('note', '')

        roles = get_jwt_claims()['roles']
        departments = get_jwt_claims()['departments']
        email = get_jwt_identity()

        if departments == 'management':
            # Retrieve all user data
            return get_leads(page=page,
                             page_size=page_size,
                             department=department,
                             priority=priority,
                             notes_offer=notes_offer,
                             sort=sort,
                             handler=''), 200
        else:
            # Non admin user can only view user's own leads.
            if email == '':
                return {
                        'isError': True,
                        'message': 'Permission denied.',
                        'statusCode': 200,
                        'data': None
                    }, 200
            else:
                return get_leads(page=page,
                                 page_size=page_size,
                                 department=departments,
                                 priority=priority,
                                 notes_offer=notes_offer,
                                 sort=sort,
                                 handler=email), 200


class LeadDetail(Resource):
    @jwt_required
    def get(self):
        leads_id = request.args.get('id')

        dealer_id = request.args.get('dealer_id')

        return get_full_lead(dealer_id, leads_id)


class LeadCreate(Resource):
    @jwt_required
    def post(self):

        dealer_id = request.form.get('dealerId', '2019123456001')
        customer_name = request.form.get('customer', 'customer')
        email = request.form.get('email', 'not available')
        phone = request.form.get('phone', 'not available')
        notes_offer = request.form.get('note', 'not available')
        appointment = request.form.get('appointment', None)

        department = request.form.get('department', 'sales')
        handler = request.form.get('handleBy', 'not available')

        priority = request.form.get('importance', 1)

        status = request.form.get('status', 'not available')

        new_leads = Lead(
            dealer_id=dealer_id,
            customer_name=customer_name,
            created=datetime.datetime.utcnow(),
            email=email,
            phone=phone,
            notes_offer=notes_offer,
            department=department,
            handler=handler,
            priority=priority,
            status=status
        )

        if appointment:
            new_leads.appointment = appointment

        print(new_leads)
        try:
            new_leads.save_to_db()

            # recipient email should be available to set dynamically !
            send_email('hzhou@blissmotors.com', 'New Leads Created', 'New Leads has been created.')

            return {
                       'isError': False,
                       'message': 'Leads is created successfully',
                       'statusCode': 200,
                   }, 200
        except Exception as e:
            print(e)

            return {'message': 'Internal Error. Please retry.'}, 500
