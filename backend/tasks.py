from celery import shared_task,Celery
from datetime import datetime,timedelta
from celery.schedules import crontab
from models import Products
import flask_excel as excel
import time
from models import Users,Bought,Products
from mail import send_message
from jinja2 import Template
from flask import request,json,copy_current_request_context
from httplib2 import Http

@shared_task(ignore_result=False)
def create_csv():
    queries= Products.query.with_entities(Products.name,Products.price,Products.quantity,Products.category_name).all()
    csv_output= excel.make_response_from_query_sets(queries,['name','price','quantity','category_name'],"csv",file_name="products.csv")
    filename="test.csv"

    with open(filename,'wb') as f:
        f.write(csv_output.data)

    return filename



@shared_task(ignore_result=True)
def monthly_report(subject):
    users=Users.query.all()
    for user in users:
        total=0
        dict={}
        price_dict={}
        items_bought=Bought.query.filter_by(user_id=user.id).all()
        sep_list=[]
        for item in items_bought:
            total+=item.quantity*item.price
            dict[item.product]=0
            price_dict[item.product]=item.price
        for item in items_bought:
            dict[item.product]+=item.quantity
        for item in dict:
            for item_ in price_dict:
                if item==item_:
                    sep_list.append([item,dict[item],price_dict[item_]])
        with open('test.html','r') as f:
            template = Template(f.read())
            send_message(user.email,subject,template.render(email=user.email,items=items_bought,total=total,monthly_items=sep_list))
    return "Remainder send"


@shared_task(ignore_result=True)
def daily_task():
    users= Users.query.all()
    for user in users:
        latest_buy=Bought.query.filter_by(user_id=user.id).order_by(Bought.date_added.desc()).first()
        last_time=latest_buy.date_added
        print('\n LATEST TIME=====================================================',latest_buy)
        now=datetime.now()
        differnce=now-last_time
        if differnce > timedelta(days=1):
            with open('daily_test.html','r') as f:
                template = Template(f.read())
        # body=last_time_str,now_str
                send_message(user.email,'Daily Remainder',template.render(user=user.username,))
    return 'Daily remainder send'