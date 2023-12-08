from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

    

class Users(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.Text())
    is_admin=db.Column(db.Boolean(),default=False)
    is_sm=db.Column(db.Boolean(),default=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlockList(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    jti=db.Column(db.String(),nullable=False)
    created_at=db.Column(db.DateTime(),default=datetime.utcnow())

    def __repr__(self):
        return f"<Token {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Products(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(30))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    category_name=db.Column(db.String(30),db.ForeignKey('categories.name'))
    category=db.relationship('Categories',backref='_products',viewonly=True,lazy='subquery')


    def __init__(self,name,price,quantity,category_name):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category_name = category_name

    def __repr__(self):
        return f"Product('{self.name}','{self.price}' ,'{self.quantity}')" 
    
    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_product_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class Categories(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(30))
    products=db.relationship('Products',backref='_category',lazy='subquery',viewonly=True)

# ,overlaps="_products,category"
    def __init__(self,name):
        self.name = name 
    
    def __repr__(self):
        return f"Category('{self.name}')"  


    def save(self):
        db.session.add(self)
        db.session.commit()

        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_category_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.Text())

    def __repr__(self):
        return f"<SM {self.username}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class user_cart(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self,user_id):
        self.user_id = user_id 
    
    def save(self):
        db.session.add(self)
        db.session.commit()




class user_items(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    u_id=db.Column(db.Integer,db.ForeignKey('user_cart.id'),nullable=False)
    # product=db.Column(db.String,db.ForeignKey('products.name'),nullable=True)
    product=db.Column(db.String(100))
    quantity=db.Column(db.Integer)
    # price=db.Column(db.Integer,db.ForeignKey('products.price'),nullable=True)
    price=db.Column(db.Integer)
    total=db.Column(db.Integer)

    def __init__(self,u_id,product,quantity,price,total):
        self.u_id = u_id 
        self.product = product 
        self.quantity = quantity 
        self.price = price 
        self.total = total 

    def save(self):
        db.session.add(self)
        db.session.commit()


class Bought(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    product=db.Column(db.String(100))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Integer)
    date_added=db.Column(db.DateTime,default=datetime.now)

    def __init__(self,user_id,product,quantity,price):
        self.user_id = user_id 
        self.product = product 
        self.quantity = quantity 
        self.price = price 

    
    def save(self):
        db.session.add(self)
        db.session.commit()


class category_creation_requests(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(30))

# ,overlaps="_products,category"
    def __init__(self,name):
        self.name = name 
    
    def __repr__(self):
        return f"Category('{self.name}')"  


    def save(self):
        db.session.add(self)
        db.session.commit()

        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class category_edit_requests(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(30))
    new_name = db.Column(db.String(30))

# ,overlaps="_products,category"
    def __init__(self,name,new_name):
        self.name = name 
        self.new_name = new_name 
    
    def __repr__(self):
        return f"Category('{self.name}')"  


    def save(self):
        db.session.add(self)
        db.session.commit()

        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class category_deletion_requests(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(30))

# ,overlaps="_products,category"
    def __init__(self,name):
        self.name = name 
    
    def __repr__(self):
        return f"Category('{self.name}')"  


    def save(self):
        db.session.add(self)
        db.session.commit()

        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # @classmethod
    # def get_category_by_name(cls, name):
    #     return cls.query.filter_by(name=name).first()


class Log(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    user=db.Column(db.String(50))
    last_online=db.Column(db.DateTime)

    def __init__(self,user,last_online):
        self.user=user
        self.last_online=last_online
        
    def save(self):
        db.session.add(self)
        db.session.commit()