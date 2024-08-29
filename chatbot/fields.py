from flask_restful import fields

message_detail_fields = {
    'id': fields.Integer,
    'customer_name': fields.String,
    'session_id': fields.String,
    'direction': fields.DateTime,
    'message': fields.List(fields.String),
    'created_time': fields.DateTime
}

message_meta_fields = {
    'id': fields.Integer,
    'customer_name': fields.String,
    'session_id': fields.String,
    'direction': fields.String,
    'message': fields.String,
    'created_time': fields.String,
    'from_user': fields.String,
    'from_bot': fields.Integer,
    'is_read': fields.Integer
}

message_list_fields = {
    'count': fields.Integer,
    'total': fields.Integer,
    'has_next': fields.Boolean,
    'data': fields.List(fields.Nested(message_meta_fields))
}

live_message_meta_fields = {
    'id': fields.Integer,
    'from_bot': fields.Integer,
    'session_id': fields.String,
    'direction': fields.String,
    'message': fields.String,
    'created': fields.String,
    'is_read': fields.Integer
}

live_message_list_fields = {
    'count': fields.Integer,
    'total': fields.Integer,
    'has_next': fields.Boolean,
    'data': fields.List(fields.Nested(live_message_meta_fields))
}

live_chat_meta_fields = {
    'id': fields.Integer,
    'from_bot': fields.Integer,
    'session_id': fields.String,
    'direction': fields.String,
    'message': fields.String,
    'imgUrl': fields.String,
    'created': fields.String,
    'from_user': fields.String,
    'un_read': fields.Integer
}

live_chat_list_fields = {
    'count': fields.Integer,
    'total': fields.Integer,
    'has_next': fields.Boolean,
    'data': fields.List(fields.Nested(live_chat_meta_fields))
}

chat_meta_fields = {
    'id': fields.Integer,
    'customer_name': fields.String,
    'session_id': fields.String,

    'device_type': fields.String,
    'device_detail': fields.String,
    'started': fields.String,
    'duration': fields.String,
    'lead': fields.Integer,
    'handler': fields.String,
    'dealer_id': fields.String,
    'dealer_name': fields.String,
    'department': fields.String,
    'missed': fields.String
}

chat_list_fields = {
    'count': fields.Integer,
    'total': fields.Integer,
    'has_next': fields.Boolean,
    'data': fields.List(fields.Nested(chat_meta_fields))
}

# chat_detail_fields = {
#     'id': fields.Integer,
#     'customer_name': fields.String,
#     'session_id': fields.String,
#
#     'device_type': fields.String,
#     'device_detail': fields.String,
#     'started': fields.DateTime,
#     'duration': fields.String,
#     'lead': fields.Integer,
#     'handler': fields.String,
#     'dealer_id': fields.String,
#     'dealer_name': fields.String,
#     'department': fields.String,
#     'missed': fields.String,
#     'messages': fields.List(fields.Nested(message_detail_fields))
# }

lead_meta_fields = {
    'id': fields.Integer,
    'dealer_id': fields.String,
    'customer_name': fields.String,
    'created': fields.String,
    'phone': fields.String,
    'email': fields.String,

    'session_id': fields.String,

    'notes_offer': fields.String,
    'appointment': fields.String,
    'handler': fields.String,
    'department': fields.String,

    'priority': fields.Integer,
    'status': fields.String
}

lead_list_fields = {
    'count': fields.Integer,
    'total': fields.Integer,
    'has_next': fields.Boolean,
    'data': fields.List(fields.Nested(lead_meta_fields))
}
