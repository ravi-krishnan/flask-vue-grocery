import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
    state:{
        results:'',
        total:0,
        cart:[],
        products:[],
        categories:[],
        logout_btn:false,
    },
    getters:{
        get_products (state){
            return state.products
        },
        get_categories (state){
            return state.categories
        },
        get_logout (state){
            return state.logout_btn
        }

    },
    mutations:{
        // for adding search queries 
        setSearchResults(state,data){
            state.results=data;
        },
        update_total(state,obj){
            state.total+=obj.count*obj.value
        },
        // generating cart products
        cart_products(state,obj){
            state.cart.push(obj)
        },
        update_products(state,obj){
            state.products=obj
        },
        update_categories(state,obj){
            state.categories=obj
        },
        update_logout(state,obj){
            state.logout_btn=obj
        }
    },
    actions:{
        async fetch_products({commit}) {
            return new Promise((resolve,reject)=>{
            fetch('http://localhost:5000/products/', { 
            method: 'GET',
            headers: {
            'Content-Type':'application/json',
            
            }})
            .then(async resp => {
            if (!resp.ok){
                const jsonresponse=await resp.json()
                throw new Error(jsonresponse.message||'Invalid Response')
            }
            return await resp.json()
            })
            .then(data =>{ 
            commit("update_products",data)
            resolve(data)
            })
            .catch(err => {
                console.log('Error: ' + err.message)
                reject(err)
            }
            
                )
            })
        },
        async fetch_categories({commit}){
            return new Promise((resolve,reject)=>{
                const token = Vue.prototype.$getCookie('access_token')
                fetch('http://localhost:5000/categories/', {
                method : 'GET',
                headers :{
                'Content-Type' : 'application/json',
                'Authentication' : `Bearer ${token}`
                },
            })
            .then(async resp => {
                if (!resp.ok){
                    const jsonresponse=await resp.json()
                    throw new Error(jsonresponse.message||'Invalid Response')
                }
                return await resp.json()
                })
                .then(data =>{ 
                console.log(data)
                commit("update_categories",data)
                resolve(data)
                })
                .catch(err => {
                    console.log('Error: ' + err.message)
                    reject(err)
                }
                )  
            })
                   
        }
    }
});


export default store