// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import jwt from 'jsonwebtoken'
import store from './store'
import Notifications from 'vue-notification'
// import './routerguard'



Vue.use(Notifications)


Vue.config.productionTip = false

Vue.prototype.$isAdmin = function(token) {
  const decoded_token=jwt.decode(token)
  return decoded_token.is_admin
}
Vue.prototype.$isSM = function(token) {
  const decoded_token=jwt.decode(token)
  return decoded_token.is_sm
}
Vue.prototype.$current_user = function(token) {
  const decoded_token=jwt.decode(token)
  return decoded_token.sub
}
function getCookie(name) {
  const value = `${document.cookie}`
  const parts = value.split(`${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

Vue.prototype.$getCookie = getCookie
/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
})
