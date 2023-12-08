from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from models import Products,Categories
from schemas import product_schema,products_schema
from extensions import db,ca
from data_access import get_all_categories,get_all_products
from time import perf_counter_ns

p_bp = Blueprint("products", __name__)

@p_bp.get('/')
@ca.cached(timeout=30,key_prefix='get_all_products_available')
def get_products():
    start=perf_counter_ns()
    products = get_all_products()
    stop=perf_counter_ns()
    print('Time Taken : ',stop-start)
    results = products_schema.dump(products)
    return jsonify(results)

# get the specific product
@p_bp.get('/<id>')
@ca.memoize(timeout=50)
def get_product(id):
    product= Products.query.get(id)
    return product_schema.jsonify(product)


#add products
@p_bp.post('/add')
@jwt_required()
def add_products():
    claims=get_jwt()
    if not claims.get('is_sm'):
        return jsonify({'message':'Access Denied'}),400
    
    name = request.json['name']
    price = request.json['price']
    quantity = request.json['quantity']
    category = request.json['category']

    if not name or not price or not quantity or not category:
        return jsonify({'message':'Incomplete Fields'}),401
    
    exist_product=Products.query.filter_by(name=name).first()
    if exist_product:
        return jsonify({
            'message':'Product already exists'
        }),402
    # query for category name is not needed  as select-option is triggered on the frontend 
    # if not Categories.query.filter_by(name=category).first():
    #     return jsonify({'message':'Category doesnt exist'}),400
    product = Products(name,price,quantity,category)
    product.save()
    return jsonify({
        'message':'Product successfully added!'
    }),200  #returning the value of the added product .. single value ie. product_schema


# edit products
@p_bp.put('/<id>')
@jwt_required()
def edit_product(id):
    claims=get_jwt()
    if not claims.get('is_sm'):
        return jsonify({'message':'Access Denied'}),409
    
    product = Products.query.get(id)

    name = request.json['name']
    price = request.json['price']
    quantity = request.json['quantity']
    category_name = request.json['category_name']
    if not name or not price or not quantity or not category_name:
        return jsonify({'message':'Incomplete fields found!'}),408
    if not Categories.query.filter_by(name=category_name).first():
        return jsonify({'message':'Category doesnt exist'}),400
    product.name = name
    product.price = price
    product.quantity = quantity
    product.category_name = category_name
    db.session.commit()
    return  jsonify(
        {
            'message': 'Product successfully edited'
        }
    ),200


#delete product
@p_bp.delete('/<id>')
@jwt_required()
def delete_product(id):
    claims=get_jwt()
    if not claims.get('is_sm'):
        return jsonify({'message':'Access Denied'}),409
    product=Products.query.get(id)
    if not product:
        return jsonify({"message":"Product does not exist"}),400
    product.delete()
    return  jsonify(
        {
            'message': 'Product successfully deleted'
        }
    ),200

@p_bp.post('/search')
def search_query():
    
    query=request.json['query']
    if  not query:
        return jsonify(
        {
            'message': 'Empy Search field'
        }
    ),400
    products=Products.query.filter(
        Products.name.ilike(f'%{query}%') 
    ).all()

    if not products:
        return jsonify(
        {
            'message': 'Product not found'
        }
    ),200 
    return products_schema.jsonify(products)



# @p_bp.get('/user')
# def get_user():
#     return current_user