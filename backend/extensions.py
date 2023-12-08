from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_caching import Cache

ma = Marshmallow()
db = SQLAlchemy()
jwt = JWTManager()
cors=CORS()
lm=LoginManager()
ca=Cache()