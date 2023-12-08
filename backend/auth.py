from flask import Blueprint, jsonify, request,make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)
from models import Users,TokenBlockList,Products,Categories,user_cart,Log
from schemas import product_schema,products_schema,categories_schema,category_schema
from extensions import db
import tasks
from datetime import datetime
from flask_login import login_user,logout_user
# from main import add_together
# import tasks

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register_user():
    data = request.get_json()

    user = Users.get_user_by_username(username=data.get("username"))
    email = Users.query.filter_by(email=data.get("email")).first()

    if user:
        return jsonify({"message": "Username taken"}), 409
    if email:
        return jsonify({"message": "Email already registered"}), 409
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({
            'message':'Empty fields found!'
        }),409
    new_user = Users(username=data.get("username"), email=data.get("email"))

    new_user.set_password(password=data.get("password"))

    new_user.save()
    new_user_cart=user_cart(user_id=new_user.id)
    new_user_cart.save()

    return jsonify({"message": "User Registered!"}), 200


# @auth_bp.delete("/user")
# @jwt_required()
# def delete_user():
#     claims=get_jwt()
    
#     if not claims.get('is_admin'):
#          return jsonify({'message':'Access Denied'}),401
    
    
#     data=request.get_json()
#     user=Users.get_user_by_username(data.get('username'))
#     if user:
#         user.delete()
#     else:
#         return jsonify({"message": "User does not exist"}),402 
#     return jsonify({"message": "Users deleted"}),204

@auth_bp.post("/login")
def login_user_():
    try:
        data = request.get_json()


        if not data:
            return jsonify({"message": "Invalid Data"}), 400
        

        user = Users.get_user_by_username(username=data.get("username"))

        if not user:
            return jsonify({"message": "User does not exist"}), 400

        if user and (user.check_password(password=data.get("password"))):

            new_log=Log.query.filter_by(user=user.username).first()
            if new_log:
                time=datetime.now()
                new_log.last_online=time
                db.session.commit()
            else:
                new_log=Log(user.username,datetime.now())
                new_log.save()
            # -----------------token creation--------------------
            additional_claims={'is_admin':user.is_admin,'is_sm':user.is_sm}
            access_token = create_access_token(identity=user.username,additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.username,additional_claims=additional_claims)
            # -----------------token creation--------------------
            login_user(user) #login user
            response= make_response(jsonify({
                "message": "Logged in as "+user.username,
                "token":{
                    "access":access_token,
                    "refresh":refresh_token
                }
                })),200
            # response.set_cookie('access_token',access_token,httponly=True)
            # response.set_cookie('refresh_token',refresh_token,httponly=True)
            # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'  # Replace with your frontend URL
            # response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
            

        return jsonify({"message": "Invalid username or password"}), 400
    
    except Exception as e:
        return jsonify({"message": str(e)}),500
        


# @auth_bp.get('/refresh')
# @jwt_required(refresh=True)
# def refresh_access():
#     identity=get_jwt_identity()
#     token=create_access_token(identity=identity)
#     return jsonify({
#         'message':token
#     })

@auth_bp.get('/logout')
@jwt_required(verify_type=False) #to aceept both access and refresh tokens
def logout():
    # if not get_jwt() :
    #     return jsonify ({'message':'No token Found'}),400
    claims=get_jwt()
    token_type=claims['type']
    jti=claims['jti']
    blocked_token=TokenBlockList(jti=jti)
    blocked_token.save()
    logout_user()
    resp = make_response(jsonify({
        'message':'Logged out',
        'token type':token_type
        
    }))
    return resp





# @auth_bp.get('/set-cookie')
# def set_cookie():
#     response = make_response("Cookie set successfully")
#     response.set_cookie('cookie_name', 'cookie_value', max_age=3600, httponly=True)
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'  # Replace with your frontend URL
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     return response


# dummy auth task route
# @auth_bp.get('/time')
# def time_worker():
#     job=tasks.say_hello.apply_async(countdown=5)
#     return str(job),200