
from flask import Blueprint, request, jsonify
login_controller = Blueprint('login-controller', __name__)
from DataAccess import UserDAL

_userDAL = UserDAL.userDAL()
@login_controller.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        formData = request.get_json()
        res = _userDAL.loginUserWithPassword(formData['username'], formData['password'])
        return jsonify(res)
    else:
        return jsonify({'not': 'found'})

@login_controller.route("/logout", methods=['POST'])
def logout():
    pass
