import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/HomePage'
import LoginPage from '@/components/LoginPage'
import RegisterUser from '@/components/RegisterUser'
import newPage from '../components/newPage.vue'
import CreateProduct from '../components/Products/CreateProduct'
import EditProduct from '@/components/Products/EditProduct'
import ProductPage from '../components/Products/ProductPage.vue'
import CreateCategory from '../components/Categories/CreateCategory'
import CategoryPage from '../components/Categories/CategoryPage'
import EditCategory from '../components/Categories/EditCategory'
import AllCategories from '../components/Categories/AllCategories'
import AdminPage from '../components/AdminPage.vue'
import SMSignup from '../components/SMSignup.vue'
import SearchPage from '../components/SearchPage.vue'
import CartPage from '../components/CartPage.vue'
import accountPage from '../components/accountPage.vue'
import SMapplicants from '../components/SMapplicants.vue'
import SMDashboard from '../components/SMDashboard.vue'
import AdminSummary from '../components/AdminSummary.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/sm',
      name: 'SMSignup',
      component: SMSignup
    },
    {
      path: '/sm/dashboard',
      name: 'SMDashboard',
      component: SMDashboard
    },
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage
    },
    {
      path: '/register',
      name: 'RegisterUser',
      component: RegisterUser
    },
    {
      path: '/account',
      name: 'accountPage',
      component: accountPage
    },
    {
      path: '/admin/summary',
      name: 'AdminSummary',
      component: AdminSummary
    },
    {
      path: '/products/add',
      name: 'CreateProduct',
      component: CreateProduct
    },
    // edit product and product page take in props

    {
      path: '/products/edit/:id',
      name: 'EditProduct',
      component: EditProduct,
      props: true
    },
    {
      path: '/products/:id',
      name: 'ProductPage',
      component: ProductPage,
      props: true
    },
    {
      path: '/categories/add',
      name: 'CreateCategory',
      component: CreateCategory
    },
    {
      path: '/categories',
      name: 'AllCategories',
      component: AllCategories
    },
    {
      path: '/categories/:id',
      name: 'CategoryPage',
      component: CategoryPage,
      props: true
    },
    {
      path: '/categories/edit/:id',
      name: 'EditCategory',
      component: EditCategory,
      props: true
    },
    {
      path: '/admin/',
      name: 'AdminPage',
      component: AdminPage
    },
    {
      path: '/search',
      name: 'SearchPage',
      component: SearchPage
    },
    {
      path: '/cart',
      name: 'CartPage',
      component: CartPage
    },
    {
      path: '/dashboard/applicants',
      name: 'SMapplicants',
      component: SMapplicants
    },
  ]
})
