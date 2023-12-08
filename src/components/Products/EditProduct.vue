<template>
    <div class="create">
    <NavBar />
    <h4 style="margin-top: 60px;">Edit Product</h4>
    <form class="center">
      <div class="form-group">
        <label for="Name">Name</label>
        <input v-model="name" class="form-control" type="text" name="Name" id="Name" placeholder="Enter Name of the Product">
      </div>
      <div class="form-group"> 
        <label for="Price">Price</label>
        <input v-model="price" class="form-control" type="number" name="Price" id="Price" placeholder="Price in Rs.">
      </div>
      <div class="form-group">
        <label for="Qauntity">Qauntity</label>
        <input  v-model="quantity" class="form-control" type="number" name="Qauntity" id="Qauntity" placeholder="Quantity in nos.">
      </div>
      <div class="form-group">
        <label for="Category">Select the category</label>
        <!-- <select name="Category" id="Category">
            <option value="Fruits">Fruits</option>
            <option value="Vegetables">Vegetables</option>
        </select> -->
        <select  v-model="category" name="Category" id="Category">Select category
            <option  v-for="category in categories" :value="category.name" :key="category.id">{{ category.name }}</option>
        </select>
      </div>
      <input class="form-control btn btn-primary" @click=UpdateProduct type="button" value="Edit">
    </form>
    
</div>
</template>
  
<script>
import NavBar from '../NavBar.vue'
import Vue from 'vue';
export default {
    beforeRouteEnter(to,from,next){
          const token = Vue.prototype.$getCookie('access_token');
          if( !token || !Vue.prototype.$isSM(token)){
              window.alert('Forbidden route')
              next('/login')
          }
          else{
              next()
          }
      },
    props: {
        id: {
        type: [Number, String],
        required: true
        }
    },
    data () {
      return{

          product : {},
          categories: [],
          name : '',
          price: null,
          quantity:null,
          category:''
         

      }
        
    },
    components :{
      NavBar: NavBar
    },
    methods :{
      loadProduct() {
        fetch(`http://localhost:5000/products/${this.id}`, {
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
          this.name=data.name
          this.quantity=data.quantity
          this.price=data.price
          this.category=data.category
        })
        .catch( err => {
          console.log(err)
          window.alert('ERRROR'+err)
        })
      },

      UpdateProduct() {
        const token = this.$getCookie('access_token')
        fetch(`http://localhost:5000/products/${this.id}`, {
          method :'PUT',
          headers : {
            'Content-Type' : 'application/json',
            'Authorization' : `Bearer ${token}`
          },
          body : JSON.stringify({
            name : this.name,
            quantity : this.quantity,
            price : this.price,
            category_name : this.category,
          })
        })
        .then(async resp =>{
          if (!resp.ok){
            const jresp = await resp.json()
            throw new Error(jresp.message || 'Invalid Response')
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
        .catch(err => {
          console.log(err)
          this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
          // window.alert('ERRRRROR' + err)
        })

      },

      getAllCategories() {
        const token = this.$getCookie('access_token')
        
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
            return resp.json()
          })
          .then(data =>{ 
            console.log(data)
            this.categories.push(...data)
          })
          .catch(err => {
            this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
            console.log('Error: ' + err.message)
          })
    },
  
  },
  created () {
    this.getAllCategories()
    this.loadProduct()
  }, 
}
</script>

<style>
/* .center{
    border: 2px solid black;
    padding: 5px;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 30%;
    margin: auto;
    transform: translate(-50%,-50%);  
}   */
</style>