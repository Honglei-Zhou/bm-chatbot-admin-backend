from flask_restful import Resource
from bot_page.handler import *
from flask import request
from .models import TodoModel, Promotion, BotConfiguration
from auth.models import BotAuth
import json
from flask_jwt_extended import jwt_required

default_page_size = 20


class CarList(Resource):

    def get(self):
        page = request.args.get('page', 1, type=int)
        dealer_id = request.args.get('dealerId')
        page_size = request.args.get('page_size', default_page_size, type=int)
        data = get_all_cars(dealer_id=dealer_id, page=page, page_size=page_size)
        return data, 200


class NewCarList(Resource):

    def get(self):
        page = request.args.get('page', 1, type=int)
        dealer_id = request.args.get('dealerId')
        page_size = request.args.get('page_size', default_page_size, type=int)
        data = get_new_cars(dealer_id=dealer_id, page=page, page_size=page_size)
        return data, 200


class UsedCarList(Resource):

    def get(self):
        page = request.args.get('page', 1, type=int)
        dealer_id = request.args.get('dealerId')
        page_size = request.args.get('page_size', default_page_size, type=int)
        data = get_used_cars(dealer_id=dealer_id, page=page, page_size=page_size)
        return data, 200


class CarDetail(Resource):

    def get(self, vin):
        dealer_id = request.args.get('dealerId')
        data = get_car_by_vin(vin, dealer_id=dealer_id)

        return data, 200


class SearchUserList(Resource):

    def get(self):
        pass


class TodoList(Resource):
    @jwt_required
    def get(self):
        data = get_todo_list()
        return data, 200


class TodoCreate(Resource):
    @jwt_required
    def post(self):
        try:
            items = request.form.get('items', [])
            if len(items) > 0:
                for item in items:
                    todo = TodoModel(
                        item=item['item'],
                        status=item['status'],
                        created=datetime.datetime.utcnow()
                    )

                    todo.save_to_db()
            else:
                item = request.form.get('item')
                status = request.form.get('status')
                todo = TodoModel(
                    item=item,
                    status=status,
                    created=datetime.datetime.utcnow()
                )

                todo.save_to_db()
            return {
                    'isError': False,
                    'message': 'Todo List is created successfully',
                    'statusCode': 200,
                    }, 200
        except Exception as e:
            print(e)

            return {'message': 'Internal Error. Please retry.'}, 500


class TodoUpdate(Resource):
    @jwt_required
    def post(self):
        try:
            items = request.form.get('items', [])

            if len(items) > 0:
                for item in items:
                    id = item['id']
                    item = item['item']
                    status = item['status']

                    current_todo = TodoModel.find_by_id(id)
                    if current_todo:
                        current_todo.item = item
                        current_todo.status = status
                        current_todo.save_to_db()
            else:
                id = request.form.get('id')
                item = request.form.get('item')
                status = request.form.get('status')

                current_todo = TodoModel.find_by_id(id)

                if current_todo:
                    current_todo.item = item
                    current_todo.status = status
                    current_todo.save_to_db()
            return {
                       'isError': False,
                       'message': 'Todo List has been updated.',
                       'statusCode': 200,
                   }, 200
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class TodoSave(Resource):
    @jwt_required
    def post(self):
        try:
            items = request.form.get('items', [])

            items = json.loads(items)

            if len(items) > 0:
                for item in items:
                    id = item.get('id')
                    item_text = item.get('item')
                    status = item.get('status')

                    current_todo = TodoModel.find_by_id(id)

                    if current_todo:
                        current_todo.item = item_text
                        current_todo.status = status
                        current_todo.save_to_db()
                    else:
                        todo = TodoModel(
                            item=item_text,
                            status=status,
                            created=datetime.datetime.utcnow()
                        )

                        todo.save_to_db()
            return {
                       'isError': False,
                       'message': 'Todo List has been updated.',
                       'statusCode': 200,
                   }, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Error. Please retry.'}, 500


class LineChart(Resource):
    @jwt_required
    def get(self):
        data = get_line_chart()
        return data, 200


class LineChartAdv(Resource):

    def get(self):
        end = request.args.get('end', datetime.datetime.utcnow())
        start = request.args.get('start', end - datetime.timedelta(days=365))
        dealer_id = request.args.get('dealerId', '2019123456001')
        data = get_line_chart_v3(start, dealer_id)
        return data, 200


class PieChart(Resource):
    @jwt_required
    def get(self):
        end = request.args.get('end', datetime.datetime.utcnow())
        start = request.args.get('start', end - datetime.timedelta(days=365))
        dealer_id = request.args.get('dealerId', '2019123456001')
        data = get_pie_chart_v2(start, dealer_id)
        return data, 200
        # data = get_pie_chart()
        # return data, 200


class BarChart(Resource):
    @jwt_required
    def get(self):
        # data = get_bar_chart()
        # return data, 200
        end = request.args.get('end', datetime.datetime.utcnow())
        start = request.args.get('start', end - datetime.timedelta(days=365))
        dealer_id = request.args.get('dealerId', '2019123456001')
        data = get_bar_chart_v2(start, dealer_id)
        print(data)
        return data, 200


class BarChartAdv(Resource):
    @jwt_required
    def get(self):
        end = request.args.get('end', datetime.datetime.utcnow())
        start = request.args.get('start', end - datetime.timedelta(days=365))
        dealer_id = request.args.get('dealerId', '2019123456001')
        data = get_bar_chart_v2(start, dealer_id)
        print(data)
        return data, 200


class UserLocation(Resource):
    @jwt_required
    def get(self):
        dealer_id = request.args.get('dealerId', '2019123456001')
        session_id = request.args.get('sessionId', '')
        return get_user_location(dealer_id, session_id), 200


class PromotionList(Resource):
    @jwt_required
    def get(self):
        dealer_id = request.args.get('dealerId')
        data = get_promotion_list(dealer_id)
        return data, 200


class PromotionCreate(Resource):
    @jwt_required
    def post(self):
        try:
            promotion_name = request.form.get('promotionName')
            dealer_id = request.form.get('dealerId')
            dealer_name = request.form.get('dealerName')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')
            code = request.form.get('code')
            coupon = request.form.get('coupon')
            keywords = request.form.get('keywords')
            note = request.form.get('note')
            department = request.form.get('department')
            valid = request.form.get('valid')

            print(start_date)
            print(end_date)
            # start_date = datetime.strptime(start_date, '%a %b %d %Y %H:%M:%S')
            # end_date = datetime.strptime(end_date, '%a %b %d %Y %H:%M:%S')
            start_date = datetime.datetime.fromtimestamp(int(start_date) / 1000.0)
            end_date = datetime.datetime.fromtimestamp(int(end_date) / 1000.0)

            promo = Promotion(
                promotion_name=promotion_name,
                dealer_id=dealer_id,
                dealer_name=dealer_name,
                start_date=start_date,
                end_date=end_date,
                code=code,
                coupon=coupon,
                keywords=keywords,
                note=note,
                department=department,
                valid=valid
            )

            promo.save_to_db()

            return {
                    'isError': False,
                    'message': 'Todo List is created successfully',
                    'statusCode': 200,
                    }, 200
        except Exception as e:
            print(e)

            return {'message': 'Internal Error. Please retry.'}, 500


class PromotionUpdate(Resource):
    @jwt_required
    def post(self):
        try:
            id = request.form.get('id')
            promotion_name = request.form.get('promotionName')
            dealer_id = request.form.get('dealerId')
            dealer_name = request.form.get('dealerName')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')
            code = request.form.get('code')
            coupon = request.form.get('coupon')
            keywords = request.form.get('keywords')
            note = request.form.get('note')
            department = request.form.get('department')
            valid = request.form.get('valid')

            start_date = datetime.datetime.fromtimestamp(int(start_date) / 1000.0)
            end_date = datetime.datetime.fromtimestamp(int(end_date) / 1000.0)

            print(id)
            print(type(id))
            current_promo = Promotion.find_by_id(id)

            if current_promo:
                current_promo.promotion_name = promotion_name
                current_promo.dealer_id = dealer_id
                current_promo.dealer_name = dealer_name
                current_promo.start_date = start_date
                current_promo.end_date = end_date
                current_promo.code = code
                current_promo.coupon = coupon
                current_promo.keywords = keywords
                current_promo.note = note
                current_promo.department = department
                current_promo.valid = valid

                current_promo.save_to_db()

            return {
                       'isError': False,
                       'message': 'Todo List has been updated.',
                       'statusCode': 200,
                   }, 200
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class PromotionDelete(Resource):
    @jwt_required
    def post(self):
        try:
            id = request.form.get('id')

            current_promo = Promotion.find_by_id(id)

            if current_promo:
                current_promo.deleted = 1

                current_promo.save_to_db()

            return {
                       'isError': False,
                       'message': 'Todo List has been updated.',
                       'statusCode': 200,
                   }, 200
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class BotConfigurationCreate(Resource):
    @jwt_required
    def post(self):
        try:
            bot_id = request.form.get('botId')
            dealer_id = request.form.get('dealerId')
            dealer_bot_name = request.form.get('dealerBotName')
            support_image = request.form.get('supportImage')
            bot_init_text = request.form.get('botInitText')
            bot_init_suggestions = request.form.get('botInitSuggestions')
            dealer_chat_window_title = request.form.get('dealerChatWindowTitle')
            dealer_title_image = request.form.get('dealerTitleImage')

            dealer_name = request.form.get('dealerName')
            dealer_address = request.form.get('dealerAddress')
            phone_numbers = request.form.get('phoneNumbers')
            sales_hours = request.form.get('salesHours')
            service_hours = request.form.get('serviceHours')
            parts_hours = request.form.get('partsHours')

            map_name = request.form.get('mapName')
            dealer_latitude = request.form.get('dealerLatitude')
            dealer_longitude = request.form.get('dealerLongitude')

            admin_name = request.form.get('adminName')
            # admin_image = request.form.get('adminImage')

            bot_configuration = BotConfiguration(
                bot_id=bot_id,
                dealer_id=dealer_id,
                dealer_bot_name=dealer_bot_name,
                support_image=support_image,
                bot_init_text=bot_init_text,
                bot_init_suggestions=bot_init_suggestions,
                dealer_chat_window_title=dealer_chat_window_title,
                dealer_title_image=dealer_title_image,
                dealer_name=dealer_name,
                dealer_address=dealer_address,
                phone_numbers=phone_numbers,
                sales_hours=sales_hours,
                service_hours=service_hours,
                parts_hours=parts_hours,
                map_name=map_name,
                dealer_latitude=dealer_latitude,
                dealer_longitude=dealer_longitude,
                # admin_image=admin_image,
                admin_name=admin_name
                )

            bot_configuration.save_to_db()

            return {
                    'isError': False,
                    'message': 'Bot Configuration is created successfully',
                    'statusCode': 200,
                    }, 200
        except Exception as e:
            print(e)

            return {'message': 'Internal Error. Please retry.'}, 500


class BotConfigurationUpdate(Resource):
    @jwt_required
    def post(self):
        try:
            bot_id = request.form.get('botId')
            dealer_bot_name = request.form.get('dealerBotName')
            support_image = request.form.get('supportImage')
            bot_init_text = request.form.get('botInitText')
            bot_init_suggestions = request.form.get('botInitSuggestions')

            dealer_chat_window_title = request.form.get('dealerChatWindowTitle')
            dealer_title_image = request.form.get('dealerTitleImage')

            dealer_name = request.form.get('dealerName')
            dealer_address = request.form.get('dealerAddress')
            phone_numbers = request.form.get('phoneNumbers')
            sales_hours = request.form.get('salesHours')
            service_hours = request.form.get('serviceHours')
            parts_hours = request.form.get('partsHours')

            map_name = request.form.get('mapName')
            dealer_latitude = request.form.get('dealerLatitude')
            dealer_longitude = request.form.get('dealerLongitude')

            admin_name = request.form.get('adminName')
            # admin_image = request.form.get('adminImage')

            current_bot = BotConfiguration.find_by_bot_id(bot_id)
            print(current_bot)

            if current_bot:
                if dealer_bot_name:
                    current_bot.dealer_bot_name = dealer_bot_name
                    current_bot.support_image = support_image
                    current_bot.bot_init_text = bot_init_text
                    current_bot.bot_init_suggestions = bot_init_suggestions
                    current_bot.admin_name = admin_name
                    # current_bot.admin_image = admin_image
                if dealer_chat_window_title:
                    current_bot.dealer_chat_window_title = dealer_chat_window_title
                    current_bot.dealer_title_image = dealer_title_image
                if dealer_name:
                    current_bot.dealer_name = dealer_name
                    current_bot.dealer_address = dealer_address
                    current_bot.phone_numbers = phone_numbers
                    current_bot.sales_hours = sales_hours
                    current_bot.service_hours = service_hours
                    current_bot.parts_hours = parts_hours
                    current_bot.map_name = map_name
                    current_bot.dealer_latitude = dealer_latitude
                    current_bot.dealer_longitude = dealer_longitude

                current_bot.save_to_db()
            else:
                current_bot = BotConfiguration()
                current_bot.bot_id = bot_id
                current_bot.dealer_id = bot_id
                
                if dealer_bot_name:
                    current_bot.dealer_bot_name = dealer_bot_name
                    current_bot.support_image = support_image
                    current_bot.bot_init_text = bot_init_text
                    current_bot.bot_init_suggestions = bot_init_suggestions
                    current_bot.admin_name = admin_name
                    # current_bot.admin_image = admin_image
                if dealer_chat_window_title:
                    current_bot.dealer_chat_window_title = dealer_chat_window_title
                    current_bot.dealer_title_image = dealer_title_image
                if dealer_name:
                    current_bot.dealer_name = dealer_name
                    current_bot.dealer_address = dealer_address
                    current_bot.phone_numbers = phone_numbers
                    current_bot.sales_hours = sales_hours
                    current_bot.service_hours = service_hours
                    current_bot.parts_hours = parts_hours
                    current_bot.map_name = map_name
                    current_bot.dealer_latitude = dealer_latitude
                    current_bot.dealer_longitude = dealer_longitude

                current_bot.save_to_db()

            return {
                       'isError': False,
                       'message': 'Todo List has been updated.',
                       'statusCode': 200,
                   }, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Error. Please retry.'}, 500


class BotConfigurationPublish(Resource):
    @jwt_required
    def post(self):
        try:
            bot_id = request.form.get('botId')
            dealer_id = request.form.get('dealerId')

            current_bot = BotAuth.find_by_bot_id(bot_id)

            current_configure = BotConfiguration.find_by_bot_id(bot_id)

            if current_bot and current_configure:
                current_configure.published = 1

                if current_configure.dealer_bot_name:
                    current_bot.dealer_bot_name = current_configure.dealer_bot_name
                    current_bot.support_name = current_configure.dealer_bot_name
                if current_configure.support_image:
                    current_bot.support_image = current_configure.support_image
                # if current_configure.admin_image:
                #     current_bot.admin_image = current_configure.admin_image
                if current_configure.admin_name:
                    current_bot.admin_name = current_configure.admin_name
                if current_configure.bot_init_text:
                    current_bot.bot_init_text = current_configure.bot_init_text
                if current_configure.bot_init_suggestions:
                    current_bot.bot_init_suggestions = current_configure.bot_init_suggestions
                if current_configure.dealer_chat_window_title:
                    current_bot.dealer_chat_window_title = current_configure.dealer_chat_window_title
                if current_configure.dealer_title_image:
                    current_bot.dealer_title_image = current_configure.dealer_title_image
                if current_configure.dealer_name:
                    current_bot.dealer_name = current_configure.dealer_name
                if current_configure.dealer_address:
                    current_bot.dealer_address = current_configure.dealer_address
                if current_configure.phone_numbers:
                    current_bot.phone_numbers = current_configure.phone_numbers
                if current_configure.sales_hours:
                    current_bot.sales_hours = current_configure.sales_hours
                if current_configure.service_hours:
                    current_bot.service_hours = current_configure.service_hours
                if current_configure.parts_hours:
                    current_bot.parts_hours = current_configure.parts_hours
                if current_configure.map_name:
                    current_bot.map_name = current_configure.map_name
                if current_configure.dealer_latitude:
                    current_bot.dealer_latitude = current_configure.dealer_latitude
                if current_configure.dealer_longitude:
                    current_bot.dealer_longitude = current_configure.dealer_longitude

                current_configure.save_to_db()
                current_bot.save_to_db()

            return {
                       'isError': False,
                       'message': 'Todo List has been updated.',
                       'statusCode': 200,
                   }, 200
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class BotConfigurationDelete(Resource):
    @jwt_required
    def post(self):
        try:
            bot_id = request.form.get('botId')

            current_configure = BotConfiguration.find_by_bot_id(bot_id)

            if current_configure:
                current_configure.published = 0

                current_configure.save_to_db()

            return {
                       'isError': False,
                       'message': 'Todo List has been updated.',
                       'statusCode': 200,
                   }, 200
        except:
            return {'message': 'Internal Error. Please retry.'}, 500


class BotConfigurationDetail(Resource):
    @jwt_required
    def get(self):
        bot_id = request.args.get('botId')
        data = get_bot_configuration(bot_id)
        return data, 200
