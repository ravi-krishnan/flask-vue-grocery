<template>
  <div class="create">
    <NavBar />
    
    <form class="center">
      <h4 class="my-5">Create new Product</h4>
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
            <!-- <option  v-for="category in categories" :value="category.name" :key="category.id">{{ category.name }}</option> -->
            <option  v-for="category in getAllCategoriesVUEX" :value="category.name" :key="category.id">{{ category.name }}</option>
        </select>
      </div>
      <input  class="form-control btn btn-primary" @click=CreateProduct type="button" value="Create">
    </form>
    
  </div>

</template>

<script>
import NavBar from '../NavBar.vue'
import Vue, { computed } from 'vue';
export default {
  beforeRouteEnter(to,from,next){
        const token = Vue.prototype.$getCookie('access_token');
        if( !Vue.prototype.$isAdmin(token) && !Vue.prototype.$isSM(token)){
            window.alert('Forbidden route')
            next('/login')
        }
        else{
            next()
        }
    },
  data () {
    return {
      name: '',
      quantity : null,
      price : null,
      category : '',
      categories : [],

    }
  },
  components :{
    NavBar :NavBar
  },
  methods :{
    
    // getAllCategories() {
    //   const token = this.$getCookie('access_token')
      
    //   fetch('http://localhost:5000/categories/', {
    //     method : 'GET',
    //     headers :{
    //       'Content-Type' : 'application/json',
    //       'Authentication' : `Bearer ${token}`
    //     },
    //   })
    //   .then(async resp => {
    //       if (!resp.ok){
    //         const jsonresponse=await resp.json()
    //         throw new Error(jsonresponse.message||'Invalid Response')
    //       }
    //       return resp.json()
    //     })
    //     .then(data =>{ 
    //       console.log(data)
    //       this.categories.push(...data)
    //     })
    //     .catch(err => console.log('Error: ' + err.message))
    // },

    CreateProduct () {
      const token = this.$getCookie('access_token')
      fetch('http://localhost:5000/products/add', {
        method :'POST',
        headers : {
          'Content-Type' : 'application/json',
          'Authorization' : `Bearer ${token}`
        },
        body : JSON.stringify({
          name : this.name,
          quantity : this.quantity,
          price : this.price,
          category : this.category,
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
    
  },
  created () {
    // this.getAllCategories()
  },
  mounted(){
    this.$store.dispatch('fetch_categories')
  },
  computed:{
    getAllCategoriesVUEX(){
      return this.$store.getters.get_categories
    }
  } 

    

  
}
</script>

<style>
  /* .center{
    
    padding: 5px;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 30%;
    margin: auto;
    transform: translate(-50%,-50%);  
} */
</style>