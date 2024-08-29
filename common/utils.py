from flask_restful import marshal


def marshal_list_data(items, has_next=False, total=0, list_fields=None, detail_fields=None):
    data = {'count': 0, 'total': total, 'has_next': has_next, 'data': []}

    if list_fields is None or detail_fields is None:
        raise Exception('list_fields and detail_fields can not be None.')
    for item in items:

        marshal_item = marshal(item, detail_fields)
        data['data'].append(marshal_item)
        data['count'] += 1
    data['total'] = total

    return marshal(data, list_fields)


def marshal_detail_data(item, has_next=False, total=1, list_fields=None, detail_fields=None):
    data = {'count': 0, 'total': total, 'has_next': has_next, 'data': []}

    if list_fields is None or detail_fields is None:
        raise Exception('list_fields and detail_fields can not be None.')

    marshal_item = marshal(item, detail_fields)
    data['data'].append(marshal_item)
    data['count'] += 1
    data['total'] = total

    return marshal(data, list_fields)
