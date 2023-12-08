from models import Users,Bought
from flask import current_app as app
from main import create_app

app = create_app()
monthly_items=[]
with app.app_context():
    users=Users.query.all()
    for user in users:
        dict={}
        items_bought=Bought.query.filter_by(user_id=user.id).all()
        for item in items_bought:
            dict[item.product]=0
        for item in items_bought:
            dict[item.product]+=item.quantity
        monthly_items.append(dict)
    print(monthly_items)
