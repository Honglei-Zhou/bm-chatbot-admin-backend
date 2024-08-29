from flask_restful import fields

user_detail_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'active': fields.Boolean,
    'created': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'roles': fields.String,
    'departments': fields.String,
    'avatar': fields.String,
    'introduction': fields.String,
    'dealer_id': fields.String,
    'dealer_url': fields.String
}

user_list_fields = {
    'count': fields.Integer,
    'total': fields.Integer,
    'has_next': fields.Boolean,
    'data': fields.List(fields.Nested(user_detail_fields))
}

bot_detail_fields = {
    'dealer_id': fields.String,
    'dealer_name': fields.String,
    'dealer_address': fields.String,
    'dealer_latitude': fields.Float,
    'dealer_longitude': fields.Float,
    'dealer_default_image': fields.String,
    'bot_init_text': fields.String,
    'bot_init_suggestions': fields.String,
    'support_name': fields.String,
    'admin_name': fields.String,

    'service_link': fields.String,
    'service_phone_number': fields.String,
    'phone_numbers': fields.String,
    'sales_hours': fields.String,
    'service_hours': fields.String,
    'parts_hours': fields.String,

    'dealer_chat_window_title': fields.String,
    'dealer_title_image': fields.String,
    'dealer_image_prefix': fields.String,
    'support_image': fields.String,
    'admin_image': fields.String,

    'dealer_info': fields.String,
    'isAuthorized': fields.Boolean
}

bot_fields = {
    'isError': fields.Boolean,
    'message': fields.String,
    'statusCode': fields.Integer,
    'isAuthorized': fields.Boolean,
    'data': fields.Nested(bot_detail_fields)
}
