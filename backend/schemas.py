from marshmallow import fields, Schema
from extensions import ma

class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.String()

class ProductSchema(ma.Schema):
    class Meta :
        fields = ('id','name','price','quantity','category_name')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class CategorySchema(ma.Schema):
    class Meta :
        fields = ('id','name')

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

class CartSchema(ma.Schema):
    class Meta:
        fields=('product','quantity','price','total')

cart_schema=CartSchema(many=True)


class EDITCATSCHEMA(ma.Schema):
    class Meta:
        fields=('id','name','new_name')

edit_categories_schema=EDITCATSCHEMA(many=True)