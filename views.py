from flask import jsonify, request
from server.server import app


@app.route("/verify", methods=['POST'])
def verify_bot():
    c_id = request.form.get('cId')
    origin = request.form.get('origin')
    # Implement method to verify the installation
    print(c_id)
    if c_id == '201978945124789':
        return jsonify(
            isError=False,
            message="Success",
            statusCode=200,
            data={'isAuthorized': True}), 200
    else:
        return jsonify(
            isError=False,
            message="Failed",
            statusCode= 200,
            data={'isAuthorized': False}), 200


@app.route("/auth", methods=['POST'])
def verify_installation():
    c_id = request.form.get('cId')
    origin = request.form.get('origin')
    # Implement method to verify the installation
    print(c_id)
    if c_id == '201978945124789':
        return jsonify(
            isError=False,
            message="Success",
            statusCode=200,
            data={'isAuthorized': True}), 200
    else:
        return jsonify(
            isError=False,
            message="Failed",
            statusCode= 200,
            data={'isAuthorized': False}), 200


@app.route("/customer/profile", methods=['POST'])
def handle_profile():
    print(request.form)
    c_id = request.form.get('cId')
    origin = request.form.get('origin')
    email = request.form.get('email')
    phone = request.form.get('phone')
    # Implement method to verify the installation
    print('{} {} {} {}'.format(c_id, origin, email, phone))
    if c_id == '201978945124789':
        return jsonify(
            isError=False,
            message="Success",
            statusCode=200,
            data={'isAuthorized': True}), 200
    else:
        return jsonify(
            isError=False,
            message="Failed",
            statusCode=200,
            data={'isAuthorized': False}), 200


@app.route("/customer/message", methods=['POST'])
def handle_text_message():
    print(request.form)
    c_id = request.form.get('cId')
    origin = request.form.get('origin')
    name = request.form.get('name')
    phone = request.form.get('phone')
    message = request.form.get('message')
    # Implement method to verify the installation
    print('{} {} {} {} {}'.format(c_id, origin, name, phone, message))
    if c_id == '201978945124789':
        return jsonify(
            isError=False,
            message="Success",
            statusCode=200,
            data={'isAuthorized': True}), 200
    else:
        return jsonify(
            isError=False,
            message="Failed",
            statusCode=200,
            data={'isAuthorized': False}), 200


@app.route("/ip", methods=['GET'])
def get_ip():
    print(request.headers.get('X-Forwarded-For', request.remote_addr))
    return request.headers.get('HTTP_X_REAL_IP', request.remote_addr), 200
