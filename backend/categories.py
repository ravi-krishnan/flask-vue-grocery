from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from models import Categories,Products,category_creation_requests,category_edit_requests,category_deletion_requests
from schemas import category_schema,categories_schema,products_schema,edit_categories_schema
from extensions import db,ca
from data_access import get_all_products,get_all_categories
from time import perf_counter_ns

c_bp = Blueprint("categories", __name__)


#get all categories

@c_bp.get('/')
@ca.cached(timeout=20,key_prefix='every_categories_that_exist')
def get_categories():
    start=perf_counter_ns()
    categories = get_all_categories()
    stop=perf_counter_ns()
    print('Time Taken : ',stop-start)
    results = categories_schema.dump(categories)
    return jsonify(results)

#get the specific category
@c_bp.get('/<id>')
@ca.memoize(timeout=50)
def get_category(id):
    category= Categories.query.get(id)
    return category_schema.jsonify(category)

#add categories
@c_bp.post('/')
@jwt_required()
def add_categories():
    claims=get_jwt()
    name = request.json['name']
    if not name:
        return jsonify({
            'message':'Incomplete field'
        }),400
    exist_category=Categories.query.filter_by(name=name).first()
    
    if exist_category:
        return jsonify({
            'message':'Category exists'
        }),401
    
    if  claims.get('is_admin'):
        category = Categories(name)
        category.save()
        return jsonify({
            'message' : 'Category created !'
        }) ,200
        # return jsonify({'message':'Access Denied'}),400
    if claims.get('is_sm'):
        # add to pending approval categories table
        pending=category_creation_requests.query.filter_by(name=name)
        if pending:
            return jsonify({
                'message':'Pending approval with the same name found'
            }),401
        pending_category=category_creation_requests(name=name)
        pending_category.save()
        return jsonify({
            'message':'Category creation approval sent'
        }),200


#edit category
@c_bp.put('/<id>')
@jwt_required()
def edit_category(id):
    claims=get_jwt()
    category = Categories.query.get(id)
    products = Products.query.filter_by(category_name=category.name)
    name = request.json['name']
    if  claims.get('is_admin'):   
        category.name = name
        for product in products:
            product.category_name=name
        db.session.commit()
        return  jsonify({
            'message' :'Category successfully edited'
        }),200
    if  claims.get('is_sm'):
        new_request = category_edit_requests(name=category.name,new_name=name)
        new_request.save()
        return jsonify({
            'message':'Category editing approval sent'
        }),200
    return jsonify({'message':'Access Denied'}),400


#delete category
@c_bp.delete('/<id>')
@jwt_required()
def delete_category(id):
    category=Categories.query.get(id)
    claims=get_jwt()

    if  claims.get('is_admin'):    
        category=Categories.query.get(id)
        products=Products.query.filter_by(category_name=category.name).all()        
        for product in products:
            product.category_name=''
            db.session.commit()
        category.delete()
        return  jsonify({
            'message' :'Category successfully deleted'
        }),200
    if  claims.get('is_sm'):
        pending=category_deletion_requests.query.filter_by(name=category.name).first()
        if pending:
            return jsonify({
                'message':'Pending approval with the same name found'
            }),401
        new_request = category_deletion_requests(name=category.name)
        new_request.save()
        return jsonify({
            'message':'Category deletion approval sent'
        }),200
    return jsonify({'message':'Access Denied'}),400


# get all products of this category
@c_bp.get('/<id>/products')
# @ca.cached(timeout=50)
def getallproducts(id):
    category= Categories.query.get(id)
    products=Products.query.filter_by(category_name=category.name).all()
    return products_schema.jsonify(products)



@c_bp.get('/requests/create')
def get_createcat_requests():
    categories=category_creation_requests.query.all()
    return categories_schema.jsonify(categories),200

@c_bp.get('/requests/edit')
def get_editcat_requests():
    categories=category_edit_requests.query.all()
    return edit_categories_schema.jsonify(categories),200

@c_bp.get('/requests/delete')
def get_deletecat_requests():
    categories=category_deletion_requests.query.all()
    return categories_schema.jsonify(categories),200


@c_bp.post('/requests/create/approve')
@jwt_required()
def approve_cat_requests():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'message':'Access Denied'}),400
    name=request.json['name']
    category=category_creation_requests.query.filter_by(name=name).first()
    category_in_cat_table=Categories.query.filter_by(name=name).first()
    if category_in_cat_table:
        category.delete()
        return jsonify({
            'message':'Category already exists'
        }),401
    else:
        new_category=Categories(name=name)
        new_category.save()
        category.delete()
        return jsonify({
            'message':'Category successfully approved'
        }),200


@c_bp.post('/requests/create/disapprove')
@jwt_required()
def disapprove_cat_requests():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'message':'Access Denied'}),400
    name=request.json['name']
    category=category_creation_requests.query.filter_by(name=name).first()
    if category:
        category.delete()
        return jsonify({
            'message':'Category successfully disapproved'
        }),200
    return jsonify({
            'message':'Unexpected error'
        }),405


@c_bp.post('/requests/edit/approve')
# this does not work, some issue from frontend
@jwt_required()
def approve_edit_cat_requests():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'message':'Access Denied'}),400
    
    name=request.json['name']
    new_name=request.json['new_name']
    category=category_edit_requests.query.filter_by(new_name=new_name).first()
    products = Products.query.filter_by(category_name=name)
    if not category:
        return jsonify({
            'message':'Request does not exist'
        }),405
    category_in_cat_table=Categories.query.filter_by(name=name).first()
    if not category_in_cat_table:
        # category.delete()
        return jsonify({
            'message':'Category does not exist'
        }),401
    
    else:

        category_in_cat_table.name=new_name
        for product in products:
            product.category_name=new_name
        category.delete()
        db.session.commit()
        return jsonify({
            'message':'Category editing successfully approved'
        }),200
    
    

@c_bp.post('/requests/edit/disapprove')
# this works tho
@jwt_required()
def disapprove_edit_cat_requests():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'message':'Access Denied'}),400
    name=request.json['name']
    category=category_edit_requests.query.filter_by(name=name).first()
    if category:
        category.delete()
        return jsonify({
            'message':'Category successfully disapproved'
        }),200
    return jsonify({
            'message':'Unexpected error'
        }),405

@c_bp.post('/requests/delete/approve')
@jwt_required()
def approve_delete_cat_requests():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'message':'Access Denied'}),400
    name=request.json['name']
    category=category_deletion_requests.query.filter_by(name=name).first()
    category_in_cat_table=Categories.query.filter_by(name=name).first()
    if category_in_cat_table:
        
        category_in_cat_table.delete()
        category.delete()
        return jsonify({
            'message':'Category deletion successfully approved'
        }),200
    else:
        category.delete()
        return jsonify({
            'message':'Category does not exists'
        }),200
    

@c_bp.post('/requests/delete/disapprove')
@jwt_required()
def disapprove_delete_cat_requests():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'message':'Access Denied'}),400
    

    name=request.json['name']
    category=category_deletion_requests.query.filter_by(name=name).first()
    if category:
        category.delete()
        return jsonify({
            'message':'Category deletion request  successfully disapproved'
        }),200
    return jsonify({
            'message':'Unexpected error'
        }),405