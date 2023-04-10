from flask import Blueprint, jsonify, request, make_response
from models import db, User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,current_user


user_blueprint = Blueprint('user_api_routes',__name__,url_prefix='/api/user')

#to get all the users
@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_user = User.query.all()
    result = [user.serialize() for user in all_user]
    response ={
        'message': 'Returning all users',
        'result': result
    }
    return jsonify(response)

@user_blueprint.route('/create', methods=['POST'])
def create_user():
#sending user data using forms for that importing request object
    try:
        user = User()
        user.username = request.form["username"]
        #password needs to be hashed using werkzeug.security
        user.password = generate_password_hash(request.form["password"],method='sha256')
        #is_Admin should be false in production
        user.is_admin = True
        db.session.add(user)
        db.session.commit()

        response = {'message': 'User Created!', 'result':user.serialize()} 
    except Exception as e:
        print(str(e))
        response = {'message': 'User Creation Failed, Error in response', 'result':str(e)}
    
    return jsonify(response)
    

@user_blueprint.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user:
        response = {'message': 'Username or password does not exist',}
        return make_response(jsonify(response),401)
    #checking if hash password stored in db is same as entered password (user.password > gett9ig hash pswd from db using user object)
    if check_password_hash(user.password, password):
        user.update_api_key()
        db.session.commit()
        #inform flask login manager that user has been logged in > import login-user
        login_user(user)
        response = {'message': 'logged in', 'api_key': user.api_key}
        #we can use to send custom headers, as well as change the property (like status_code , mimetype , etc.) in response
        return make_response(jsonify(response),200)
    
    response = {'message': 'Access Denied',}
    return make_response(jsonify(response),401)

@user_blueprint.route('/logout',methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'Logged out successfully'})
    return jsonify({'message': 'No user logged in'}), 401

@user_blueprint.route('/<username>/exists',methods=['GET'])
def user_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'result': True}), 200
    
    return jsonify({'result':False}),404

@user_blueprint.route('/',methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'result': current_user.serialize()}), 200
    else:
        return jsonify({'message':'User not logged in'}), 401