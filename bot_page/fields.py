from flask_restful import fields

car_detail_fields = {
    # 'dealer_id': fields.String,
    # 'dealer_name': fields.String,
    'vin': fields.String,
    'stock': fields.String,
    'new_used': fields.String,
    'year': fields.Integer,
    'make': fields.String,
    'model': fields.String,
    'model_number': fields.String,
    'body': fields.String,
    'transmission': fields.String,
    'series': fields.String,
    'body_door_ct': fields.Integer,
    'odometer': fields.Integer,
    'engine_cylinder_ct': fields.Integer,
    'engine_displacement': fields.String,
    'drivetrain_desc': fields.String,
    'colour': fields.String,
    'interior_color': fields.String,
    'msrp': fields.Float,
    'price': fields.Float,
    'inventory_date': fields.String,
    'certified': fields.String,
    'description': fields.String,
    'features': fields.List(fields.String),
    'photo_url_list': fields.List(fields.String),
    'city_mpg': fields.Float,
    'highway_mpg': fields.Float,
    # 'photos_last_modified_date': fields.String,
    # 'series_detail': fields.String,
    'engine': fields.String,
    'fuel': fields.String,
    # 'age': fields.Integer
    'link': fields.String
}

car_fields = {
    # 'dealer_id': fields.String,
    # 'dealer_name': fields.String,
    'vin': fields.String,
    'stock': fields.String,
    'new_used': fields.String,
    'year': fields.Integer,
    'make': fields.String,
    'model': fields.String,
    'model_number': fields.String,
    'body': fields.String,
    'transmission': fields.String,
    'series': fields.String,
    'body_door_ct': fields.Integer,
    'odometer': fields.Integer,
    'engine_cylinder_ct': fields.Integer,
    'engine_displacement': fields.String,
    'drivetrain_desc': fields.String,
    'colour': fields.String,
    'interior_color': fields.String,
    'msrp': fields.Float,
    'price': fields.Float,
    'inventory_date': fields.String,
    'certified': fields.String,
    # 'description': fields.String,
    # 'features': fields.List(fields.String),
    'photo_url_list': fields.List(fields.String),
    'city_mpg': fields.Float,
    'highway_mpg': fields.Float,
    # 'photos_last_modified_date': fields.String,
    'series_detail': fields.String,
    'engine': fields.String,
    'fuel': fields.String,
    'link': fields.String
    # 'age': fields.Integer
}

car_list_fields = {
    'count': fields.Integer,
    'total': fields.Integer,
    'has_next': fields.Boolean,
    'data': fields.List(fields.Nested(car_fields))
}

car_list_detail_fields = {
    'count': fields.Integer,
    'has_next': fields.Boolean,
    'data': fields.List(fields.Nested(car_detail_fields))
}

webuser_fields = {
    'session_id': fields.String,
    'city': fields.String,
    'state': fields.String,
    'device_type': fields.String,
    'device_detail': fields.String
}

webuser_list_fields = {

}

new_visits_fields = {
    'name': fields.String,
    'data': fields.List(fields.Integer),
    'x_axis': fields.List(fields.String),
    'legend': fields.String
}

messages_fields = {
    'name': fields.String,
    'data': fields.List(fields.Integer),
    'x_axis': fields.List(fields.String),
    'legend': fields.String
}

chat_sessions_fields = {
    'name': fields.String,
    'data': fields.List(fields.Integer),
    'x_axis': fields.List(fields.String),
    'legend': fields.String
}


new_visits_list_fields = {
    'name': fields.String,
    'date': fields.List(fields.String),
    'city': fields.List(fields.String),
    'legend': fields.String
}

messages_list_fields = {
    'name': fields.String,
    'date': fields.List(fields.String),
    'direction': fields.List(fields.String),
    'legend': fields.String
}

chat_sessions_list_fields = {
    'name': fields.String,
    'date': fields.List(fields.String),
    'legend': fields.String
}

line_chart_fields = {
    'newVisits': fields.Nested(new_visits_fields),
    'messages': fields.Nested(messages_fields),
    'chatSessions': fields.Nested(chat_sessions_fields)
}

line_chart_fields_adv = {
    'newVisits': fields.Nested(new_visits_list_fields),
    'messages': fields.Nested(messages_list_fields),
    'chatSessions': fields.Nested(chat_sessions_list_fields)
}

pie_chart_value_fields = {
    'value': fields.Integer,
    'name': fields.String
}

pie_chart_value_fields_v2 = {
    'date': fields.String,
    'value': fields.Integer,
    'name': fields.String
}

pie_chart_fields = {
    'data': fields.List(fields.Nested(pie_chart_value_fields))
}

pie_chart_fields_v2 = {
    'data': fields.List(fields.Nested(pie_chart_value_fields_v2))
}

bar_chart_value_fields = {
    'name': fields.String,
    'data': fields.List(fields.Integer),
    'legend': fields.String,
}

bar_chart_fields = {
    'name': fields.String,
    'data': fields.List(fields.Nested(bar_chart_value_fields)),
    'x_axis': fields.List(fields.String)
}

todo_fields = {
    'id': fields.Integer,
    'text': fields.String,
    'done': fields.Boolean
}

todo_list_fields = {
    'total': fields.Integer,
    'items': fields.List(fields.Nested(todo_fields))
}

promotion_fields = {
    'id': fields.Integer,
    'promotion_name': fields.String,
    'dealer_id': fields.String,
    'dealer_name': fields.String,
    'code': fields.String,
    'coupon': fields.String,
    'keywords': fields.String,
    'note': fields.String,
    'department': fields.String,
    'start_date': fields.String,
    'end_date': fields.String,
    'created': fields.String,
    'valid': fields.Integer
}

promotion_list_fields = {
    'total': fields.Integer,
    'promotions': fields.List(fields.Nested(promotion_fields))
}


bot_configuration_fields = {
    'bot_id': fields.String,
    'dealer_id': fields.String,

    'dealer_bot_name': fields.String,
    'admin_name': fields.String,
    'support_image': fields.String,
    'bot_init_text': fields.String,
    'bot_init_suggestions': fields.String,

    'dealer_chat_window_title': fields.String,
    'dealer_title_image': fields.String,

    'dealer_name': fields.String,
    'dealer_address': fields.String,
    'phone_numbers': fields.String,
    'sales_hours': fields.String,
    'service_hours': fields.String,
    'parts_hours': fields.String,

    'map_name': fields.String,
    'dealer_latitude': fields.Float,
    'dealer_longitude': fields.Float,

    'published': fields.Integer
}
