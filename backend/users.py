from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from models import Users,user_items,Bought,Products
from schemas import UserSchema,cart_schema,products_schema
from extensions import db,ca
from datetime import datetime

user_bp = Blueprint("users", __name__)


@user_bp.get("/all")
@jwt_required()
@ca.memoize(timeout=50)
def get_all_users():
    token=request.cookies.get('access_token')
    claims=get_jwt()

    if not claims.get('is_admin'):
         return jsonify({'message':'Access Denied'}),409
    
    users=Users.query.all()
    result = UserSchema().dump(users, many=True)

    return (
        jsonify(result),
        200,
    )


@user_bp.get('/<user>/cart')
@ca.memoize(timeout=10)
def get_cart(user):
    cart_user=Users.query.filter_by(username=user).first()
    cart_items=user_items.query.filter_by(u_id=cart_user.id).all()
    return cart_schema.jsonify(cart_items)





@user_bp.post('/<user>/cart')
def add_to_cart(user):
    user=Users.query.filter_by(username=user).first()
    name=request.json['name']
    value=request.json['value']
    count=request.json['count']
    prod_exist=user_items.query.filter_by(u_id=user.id,product=name).first()
    product_info=Products.query.filter_by(name=name).first()
    if product_info.quantity-count<0:
        return jsonify({
            'message':'Out of Stock'
        }),404
    if prod_exist:
        prod_exist.quantity=prod_exist.quantity+count
        prod_exist.total=prod_exist.total+count*value
        product_info.quantity=product_info.quantity-count
        db.session.commit()
        return jsonify({
        'message':'Items added to cart'
        }),200
    
    else:
        new_user_item=user_items(u_id=user.id,product=name,quantity=count,price=value,total=count*value)
        product_info.quantity=product_info.quantity-count
        new_user_item.save()
        db.session.commit()

        return jsonify({
            'message':'Item added to cart'
        }),200

    return jsonify({
        'message':'Unexpected error'
    }),404

@user_bp.post('/<user>/bought')

def user_checkout(user):
    user=Users.query.filter_by(username=user).first()
    data=request.get_json()
    items=data['items']
    if not items:
        return jsonify({
            'message':'Unexpected error'
        }),405
    for item in items:
        # print(item['product'])
        db.session.add(Bought(
            user_id=user.id,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price'],
            # date_added=datetime.now
            ))
    u_items=user_items.query.filter_by(u_id=user.id).all()
    for u_item in u_items:
        db.session.delete(u_item)
    db.session.commit()
    # return jsonify(data['items']),200
    return jsonify({
        'message':'Successfully Checked Out'
    }),200



@user_bp.get('/<username>/account')
@ca.memoize(timeout=60)
def account_page(username):
    # user=Users.get(username)
    user=Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            'message':'User not found'
        }),401
    return jsonify({
        'user':user.username,
        'email':user.email,
        'sm':user.is_sm
    }),200