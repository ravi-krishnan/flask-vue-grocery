<template>
  <div>
    <NavBar />
    <div class="row" style="margin-top: 60px;">
    <div class="col-sm-3" v-for="product in this.getProductsVUEX" :key="product.id ">
    <!-- <div class="col-sm-3" v-for="product in this.products" :key="product.id ">            -->
        <div class="card">
          <div class="card-body" >
            <router-link :to="`/products/${product.id}`"><h5 class="card-title">{{ product.name }}</h5></router-link>
            <h6 class="card-text">Rs.{{ product.price }}</h6>
            <h6 class="card-text">Quantity: {{ product.quantity }}</h6> 
            <h6 class="card-text">Category: {{ product.category_name }}</h6> 
            <a  class="btn btn-success btn-sm" @click="toggleInputFn">Buy</a>
            <div v-if="toggleInput">
                <input type="number" v-model.number="count[product.id]" placeholder="enter the number of products required">
                <a  class="btn btn-success btn-sm" @click="addtoCart(count[product.id],product.price,product.name,current_user)">Add to Cart</a>
            </div>

          </div>
        </div>
      </div>
      
       <br> <br>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
// import { computed } from 'vue'
export default {
  name: 'HomePage',
  data () {
    return {
      count:[],
      Products:[],
      products:[],
      sm:false,
      admin:false,
      toggleInput:false,
      current_user:null
    }
  },
  components: {
    NavBar
  },
  methods: {
    // getProducts(){
    //   this.Products= this.$store.getters.get_products
    // },
    // add to vuex cart
    // addtoCart(count,value,name){
    //   // console.log(count,value,id)
    //   this.$store.commit("update_total",{"count":count,"value":value})
    //   this.$store.commit("cart_products",{"name":name,"count":count,"value":value})

    // },
    addtoCart(count,value,name,current_user){
      if (!current_user){
        this.$notify({
                    group: 'warning',
                    type: 'warn',
                    text: 'Login to do this action',
            })
        this.$router.push('/login')
      }
      else{
        const token=this.$getCookie('access_token')
      fetch(`http://localhost:5000/users/${current_user}/cart`,{
        method:'POST',
        headers:{
          'Content-Type':'application/json',
          'Authorization':`Bearer ${token}`
        },
        body:JSON.stringify({
          count:count,
          value:value,
          name:name
        })
      })
      .then(resp=>resp.json())
      .then(data=>{
        this.$notify({
                    group: 'success',
                    type: 'success',
                    text: data.message,
            })
        console.log(data)
      })
      .catch(err=>{
        this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
        console.log(err)
        })
      }
      
    },
    toggleInputFn() {
      this.toggleInput = !this.toggleInput
    },
    loadcurrentuser() {
      try{
        const token = this.$getCookie('access_token')
        this.sm=this.$isSM(token)
        this.admin=this.$isAdmin(token)
        this.current_user=this.$current_user(token)
      }
      catch(err){
        // this.$notify({
        //             group: 'fail',
        //             type: 'error',
        //             text: err,
        //     })
        console.log(err)
      }
        
    },
    // getAllProducts () {
    //   const token = this.$getCookie('access_token') 
    //       fetch('http://localhost:5000/products/', { 
    //       method: 'GET',
    //       headers: {
    //         'Content-Type':'application/json',
    //         // 'Authorization': `Bearer ${token}`,
            
    //     }})
    //     .then(async resp => {
    //       if (!resp.ok){
    //         const jsonresponse=await resp.json()
    //         throw new Error(jsonresponse.message||'Invalid Response')
    //       }
    //       return resp.json()
    //     })
    //     .then(data =>{ 
    //       // console.log(data)
    //       this.products.push(...data)
    //     })
    //     .catch(err => console.log('Error: ' + err.message))

    //   },
    },
    created () {
      // this.getAllProducts()
      this.loadcurrentuser()
      // this.$store.dispatch("fetch_products")
      // this.getResponse()
    },
    mounted () {
      this.$store.dispatch('fetch_products')
      this.$store.dispatch('fetch_categories')
    },
    computed:{
      getProductsVUEX() {
        return this.$store.getters.get_products
      }
    }
}
  
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
