# export csv works, but after exporting, whole app resets..
from flask import Flask, jsonify,send_file
from extensions import db, jwt,cors,ma,lm,ca
from auth import auth_bp
from users import user_bp
from admin import admin_bp
from products import p_bp
from categories import c_bp
from sm import sm_bp
from flask_cors import CORS
from models import TokenBlockList,Users,user_cart,Products
from werkzeug.security import check_password_hash,generate_password_hash
import workers
import tasks
import flask_excel as excel
from celery.result import AsyncResult
from celery.schedules import crontab
from flask_login import LoginManager,login_user,logout_user,current_user

def create_app():
    app = Flask(__name__)
    # ===========================CONFIG===================================
    app.config['SECRET_KEY']="123214asd12421"
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
    app.config['SQLALCHEMY_ECHO']=True
    app.config['JWT_SECRET_KEY']="56d178c74ef2b3a447fc4c32"
    app.config['DEBUG']=True
    app.config['CACHE_TYPE']="RedisCache"
    app.config['CACHE_REDIS_HOST']="localhost"
    app.config['CACHE_REDIS_PORT']=6379
    # ===========================CONFIG===================================
    ma.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    lm.init_app(app)
    ca.init_app(app)
    excel.init_excel(app)
    # register bluepints
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(p_bp, url_prefix="/products")
    app.register_blueprint(c_bp, url_prefix="/categories")
    app.register_blueprint(sm_bp, url_prefix="/sm")

    with app.app_context():
        db.create_all()
        if not Users.get_user_by_username(username='Admin'):
            admin=Users(username='Admin',email='admin@gmail.com',is_admin=True,is_sm=False)
            admin.set_password('12345')
            admin.save()
            admin_cart=user_cart(user_id=admin.id)
            admin_cart.save()

# ==========================================================================================================================
    @lm.user_loader
    def load_user(user_id):
        return Users.get(user_id)

    # @jwt.additional_claims_loader
    # def adding_claims(identity):
    #     if identity=='ravi':
    #         return {'is_admin':True}
    #     else:
    #         return {'is_admin':False}

        
    #jwt error handling

    @jwt.expired_token_loader
    def expired_token(jwt_header,jwt_data):
        return jsonify({'message':'Token expired',
                        'error':'expired_token'}),401
    
    @jwt.invalid_token_loader
    def invalid_token(error):
        return jsonify({'message':'Invalid Token ',
                        'error':'invalid_token'}),401

    @jwt.unauthorized_loader
    def missing_token(error):
        return jsonify({'message':'Missing Token',
                        'error':'missing_token'}),401
     
    #jwt token block list error handling
    
    @jwt.token_in_blocklist_loader
    def token_in_blocklist(jwt_header,jwt_data):
        jti=jwt_data['jti']
        token = db.session.query(TokenBlockList).filter(TokenBlockList.jti==jti).scalar()
        return token is not None

# ==========================================================================================================================

    return app

app=create_app()
celery_app=workers.celery_init_app(app)

@celery_app.on_after_configure.connect
def send_email(sender,**kwargs):
    sender.add_periodic_task(10.0,tasks.monthly_report.s('Monthly Report'),name='Monthly Report')
    # sender.add_periodic_task(crontab(day_of_month='1',hour='17',minute='30'),tasks.monthly_report.s('Monthly Report'),name='Monthly Report')
    sender.add_periodic_task(10.0,tasks.daily_task.s(),name='Daily Task')
    # sender.add_periodic_task(crontab(hour='16',minute='30'),tasks.daily_task.s(),name='Daily Webhook Task') # works




    
    

# # 
if __name__ == "__main__":
    # app, celery = create_app()
    app.run(debug=True,threaded=True)

