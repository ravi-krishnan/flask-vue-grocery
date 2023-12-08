from flask import send_file,Blueprint,jsonify
import matplotlib.pyplot as plt
from io import BytesIO
from models import Products,Bought,Categories
from celery.result import AsyncResult
import tasks
sm_bp=Blueprint("sm",__name__)

def generate_bar_recent_chart():

    x=[item.name for item in Products.query.all()]
    value_init={}
    for item in x:
        value_init[item]=0
    for item in x:
        for i in Bought.query.filter_by(product=item).all():
            value_init[item]=value_init[item]+i.quantity
    y=[value_init[item] for item in x]
    # y=[(Bought.query.filter_by(product=item).all()) for item in x]
    plt.bar(x,y)
    plt.xlabel('Products')
    plt.ylabel('No. of times bought')

    # save
    img = BytesIO()
    plt.savefig(img,format='png')
    img.seek(0)
    plt.close()

    return img


def generate_py_chart():

    labels=[item.name for item in Categories.query.all()]
    values=[len(Products.query.filter_by(category_name=category).all()) for category in labels]
    total=0
    for val in values:
        total=total+val
    weight=[(val/total) for val in values]
    fig,ax=plt.subplots()
    ax.pie(weight,labels=labels,startangle=90)
    ax.axis('equal')

    img2=BytesIO()
    plt.savefig(img2,format='png')
    img2.seek(0)
    plt.close()

    return img2


@sm_bp.get('/chart/recent_buy')

def recent_by():
    
    img = generate_bar_recent_chart()

    return send_file(img,mimetype='image/png')


@sm_bp.get('/chart/pie')
def pie_chart():
    img2 = generate_py_chart()

    return send_file(img2,mimetype='image/png')




@sm_bp.get('/res/<id>')
def getii(id):
    result =AsyncResult(id)

    r = {
        'ready':result.ready(),
        'result':result.result if result.ready() else  None
    }
    return r


@sm_bp.get('/download-csv')
def download():
    try:
        task = tasks.create_csv.delay()
        return jsonify({'task_id':task.id}),200
    except:
        return jsonify({'message':'error'}),400


@sm_bp.get('/csv/<id>')
def getcsv(id):
    result =AsyncResult(id)
    if result.ready():
        filename=result.result
        return send_file(filename,as_attachment=True),200
    else:
        return jsonify({'message':'Task pending'}),404