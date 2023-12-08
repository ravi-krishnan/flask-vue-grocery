# Grocery Store App

> A Vue.js + Flask project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).


## Functions

* Ability to browse and buy multiple products across a wide range of categories.
* The app uses Admin, Store Manager and user roles.
* Only Admin holds access to create, update or delete categories
* Only Store Managers can create, update or delete products.
* Changes to the categories can be requested by Store Managers
* Users also have the option to register as store managers, however access is granted only after Admin approval.
* Store Managers can download inventory details from their dashboard
* From the Store Manager dashboard, we can get a glimpse of the distribution of products and categories and also the most popular products
* From the Admin dashboard , we can see user activities and checkout details
* Daily remainder and  Monthly reports are sent to each user based on their activity (using celery+Redis)
