<template>
    <div>
        <NavBar></NavBar>
        <div class="row" style="margin-top: 30px; border: 2px dotted rgb(141, 139, 139);background-color:rgb(214, 214, 219) ;">
          <div class="col ">
            <h3>{{ name }}</h3>
          </div>
          <div class="col">
            <div v-if="admin || sm" >
              <button class="btn btn-danger" data-toggle="modal" data-target="#deleteModal">Delete</button>
              <router-link :to="`/categories/edit/${id}`" class="btn btn-warning">Edit</router-link>
          </div>
          </div>
          
        </div>
        
        <div class="row" style="margin-top: 40px;" >
          <div class="col-sm-3" v-for="product in products" :key="product.id">
            <div class="card">
              <div class="card-body" >
                <router-link :to="`/products/${product.id}`"><h5 class="card-title">{{ product.name }}</h5></router-link>
                <h6 class="card-text">Rs.{{ product.price }}</h6>
                <h6 class="card-text">Quantity: {{ product.quantity }}</h6> 
                <h6 class="card-text">Category: {{ product.category_name }}</h6> 
                <!-- <a  class="btn btn-success btn-sm" @click="toggleInputFn">Buy</a> -->
                <!-- <div v-if="toggleInput">
                  <input type="number" v-model.number="count[product.id]" placeholder="enter the number of products required"> -->
                  <!-- <a  class="btn btn-success btn-sm" @click="addtoCart(count[product.id],product.price,product.name,current_user)">Add to Cart</a> -->
                 
              </div>
              </div>
            </div>
          </div>
          
          <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="deleteModalLabel">Delete Category?</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                      <form>
                        <input @click="this.deleteCategory" class="btn btn-danger" type="submit" value="Delete">
                      </form>
                    </div>
                  </div>
                </div>
              </div>
</div>

        


        <!-- <h3>{{ name }}</h3>
        <br> <br> -->
       
        

        <!-- <h2>Products</h2> -->
        <!-- <p v-for="product in products" :key="product.id">
          <router-link :to="`/products/${product.id}`">{{ product.name }}</router-link>
        </p> -->
    
</template>

<script>
// import Vue from 'vue';
import NavBar from '../NavBar.vue'
export default {    
    // beforeRouteEnter(to,from,next){
    //       const token = Vue.prototype.$getCookie('access_token');
    //       if( !token || !Vue.prototype.$isAdmin(token)){
    //           window.alert('Forbidden route')
    //           next('/login')
    //       }
    //       else{
    //           next()
    //       }
    //   },
    data () {
        return {
          admin: '',           
          name : '',
          products:[],
          sm:''
        }
    },
    props:{
        id : {
            type: [Number, String],
            required: true
        }
    },
    components:{
        NavBar :NavBar
    },
    methods:{
        loadcurrentuser() {
          const token = this.$getCookie('access_token')
          this.admin=this.$isAdmin(token)
          this.sm=this.$isSM(token)
        },
        loadProducts(){
          fetch(`http://localhost:5000/categories/${this.id}/products`, {
          methods : 'GET',
          headers: {
            'Content-Type' : 'application/json'
          }
        })
        .then( async resp =>{
          if (!resp.ok){
            const jresp = resp.json()
            throw new Error (jresp.message || 'invlaid response')
          }
          return resp.json()
        })
        .then(data => {
          console.log(data)
          this.products.push(...data)
        })
        .catch( err => {
          console.log(err)
          this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
          // window.alert('ERRROR'+err)
        })
        },
        loadCategory() {
        fetch(`http://localhost:5000/categories/${this.id}`, {
          methods : 'GET',
          headers: {
            'Content-Type' : 'application/json'
          }
        })
        .then( async resp =>{
          if (!resp.ok){
            const jresp = resp.json()
            throw new Error (jresp.message || 'invlaid response')
          }
          return resp.json()
        })
        .then(data => {
          // console.log(data)
          this.name=data.name
        })
        .catch( err => {
          console.log(err)
          this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
          // window.alert('ERRROR'+err)
        })
      },


      deleteCategory() {
        const token =this.$getCookie('access_token')
        fetch(`http://localhost:5000/categories/${this.id}`, {
          method : 'DELETE',
          headers: {
            'Content-Type' : 'application/json',
            'Authorization':`Bearer ${token}`
          }
        })
        .then( async resp =>{
          if (!resp.ok){
            const jresp = await resp.json()
            throw new Error (jresp.message || 'invlaid response')
          }
          return resp.json()
        })
        .then(data => {
          console.log(data)
          this.$notify({
                    group: 'success',
                    type: 'success',
                    text: data.message,
            })
        })
        .catch( err => {
          console.log(err)
          // window.alert('ERRROR'+err)
          this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
        })
      },
    },
    mounted (){
        this.loadCategory()
        this.loadcurrentuser()
        this.loadProducts()
    }
}   
</script>

<style>
  
</style>