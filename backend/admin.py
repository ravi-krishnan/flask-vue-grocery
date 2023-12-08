from flask import Blueprint, jsonify, request,make_response,send_file
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
)
from models import Users,TokenBlockList,Products,Categories,Applicants,user_cart,Log,Bought
from io import BytesIO
import datetime
import matplotlib.pyplot as plt
from extensions import ma,db
from io import BytesIO
admin_bp = Blueprint("admin", __name__)


class ApplicantSchema(ma.Schema):
    class Meta :
        fields = ('username','email','password')

applicants_schema = ApplicantSchema(many=True)


@admin_bp.get('/sm/requests')
@jwt_required()
def get_requests():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'message':'Access Denied'}),409
    
    applicants =Applicants.query.all()
    return applicants_schema.jsonify(applicants),200
    

    

@admin_bp.post('/sm/requests')
def submit_requests():
    data=request.get_json()
    user = Applicants.get_user_by_username(username=data.get("username"))

    if user is not None:
        return jsonify({"message": "Application already exists"}), 409

    new_user = Applicants(username=data.get("username"), email=data.get("email"))

    new_user.set_password(password=data.get("password"))

    new_user.save()

    return jsonify({'message':'Application Submitted Successfully '}),200


@admin_bp.post('/sm/approve')
@jwt_required()
def create_sm():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({
        'message' : 'Access Denied',
    }),409
    applicant=Applicants.query.filter_by(username=request.json['username']).first()
    if not applicant:
        return jsonify({
        'message' : 'Application does not exist',
    }),409
    user = Users.query.filter_by(username=request.json['username']).first()
    if user:
        if user.is_sm:
            return jsonify({
            'message' : 'Application already approved',
        }),409
        user.is_sm=True
        applicant.delete()
        db.session.commit()
        return jsonify({
            'message' : 'Application Approved!',
        }),200
    new_sm=Users(username=applicant.username,password=applicant.password,email=applicant.email,is_admin=False,is_sm=True)
    new_sm.save()
    new_sm_cart=user_cart(user_id=new_sm.id)
    new_sm_cart.save()
    applicant.delete()
    return jsonify({
        'message' : 'Application Approved!',
    }),200

@admin_bp.post('/sm/disapprove')
@jwt_required()
def de_sm():
    claims=get_jwt()
    if not claims.get('is_admin'):
        return jsonify({
        'message' : 'Access Denied',
    }),409
    applicant=Applicants.query.filter_by(username=request.json['username']).first()
    if not applicant:
        return jsonify({
        'message' : 'Application does not exist!',
    }),409
    applicant.delete()
    # need to send user the message of dissaproval
    return jsonify({
        'message' : 'Application disapproved successfully!',
    }),200



def get_log_report():
    active=[]
    inactive=[]
    for user in Log.query.all():
        if datetime.datetime.now()-user.last_online < datetime.timedelta(minutes=7):
            active.append(user)
        else:
            inactive.append(user)
    labels=['Active','Inactive']

    if len(active)+len(inactive)==0:
        return 'zero-division'
    weights=[len(active)/len(active)+len(inactive),len(inactive)/len(active)+len(inactive)]

    plt.pie(weights,labels=labels,startangle=90)

    img3 = BytesIO()
    plt.savefig(img3,format='png')
    img3.seek(0)

    plt.close()

    return img3


@admin_bp.get('/chart/active')
def get_active_users():

    img3=get_log_report()
    if img3=='zero-division':
        return jsonify({
            'message':'No active users for a while now'
        })
    return send_file(img3,mimetype='image/png')


def get_best_report():
    labels=[user.user_id for user in Bought.query.all()]
    x=[Users.query.get(user).username for user in labels]
    y=[len(Bought.query.filter_by(user_id=user).all()) for user in labels]
    plt.bar(x,y)
    plt.xlabel('Users')
    plt.ylabel('No.times checked out')


    img4=BytesIO()

    plt.savefig(img4,format='png')
    img4.seek(0)
    plt.close()

    return img4

@admin_bp.get('/chart/best')
def get_best_users():

    img4=get_best_report()

    return send_file(img4,mimetype='image/png')