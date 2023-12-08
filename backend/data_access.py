from models import Users,Products,Categories
from extensions import ca


@ca.cached(timeout=30,key_prefix='get_all_products')
def get_all_products():
    products= Products.query.all()
    return products



@ca.cached(timeout=30,key_prefix='get_all_categories')
def get_all_categories():
    categories= Categories.query.all()
    return categories

