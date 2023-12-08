<template>
  <div>
    <NavBar></NavBar>
    <!-- <h4>Cart  : {{ getCartProducts }}</h4> -->
    <div v-if="items.length>0" class="container" style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr;">
      <div>Name</div>
      <div>Price</div>
      <div>Quantity</div>
      
      <div>Total</div>

    </div>
    <div  class="items" v-for="product in items" :key="product.name">
      <div class="container">
        <div class="item ">{{ product.product }}</div>
        <div class="item">₹{{ product.price }}</div>
        <div class="item ">{{ product.quantity }}</div>
        
        <div class="item"  >₹{{ product.total }}</div>
      </div>
      

        
      <!-- {{calculate_total(product.total)}} -->
    </div>
    
    <!-- {{this.calculate_total(product.total)}} -->
    <h4 v-if="items.length>0"> Grand Total : ₹{{ calculate_total()}}</h4>
    <button v-if="items.length>0" @click="checkoutItems" class="btn btn-success">Checkout</button>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'
export default {
    data(){
      return {
        current_user:null,
        items:[],
        // total: 0,
        count:0,
        // checkout:false,
      }
    },
    components:{
        NavBar
    },
    methods:{
      checkoutItems(){
        // eneter fetch
        const token=this.$getCookie('access_token')
        const current_user=this.$current_user(token)
        fetch(`http://localhost:5000/users/${current_user}/bought`,{
          method:'POST',
          headers:{
            'Content-Type':'application/json',
            // 'Authorization':`Bearer ${token}`
          },
          body:JSON.stringify({
            items:this.items
          })
        })
        .then(resp => resp.json())
        .then(data=>{
          console.log(data)
          this.$notify({
              group: 'success',
              type: 'success',
              text: data.message,
            })
          setTimeout(()=>{
            this.$router.push('/')
          },1000)
        })
        .catch(err=>{
          console.log(err)
          this.$notify({
              group: 'fail',
              type: 'error',
              text: err,
            })
        })
      },
      calculate_total(){
        let total = 0
        for (let item of this.items){
          total  += item.total
        }
        return total
      },
      getCartProducts(){
        const token=this.$getCookie('access_token')
        const current_user=this.$current_user(token)
        fetch(`http://localhost:5000/users/${current_user}/cart`,{
          method:'GET',
          headers:{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${token}`
          }
        })
        .then(resp=>resp.json())
        .then(data=>{
          // console.log(data)
          this.items.push(...data)
          // this.checkout=true
        })
        .catch(err=>{
          this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
          console.log(err)})

      }
    },
    computed:{
        getcheckout(){
          return this.items
        }
      // getTotal(){
      //   return this.$store.state.total
      // },
      
    },
    mounted(){
      this.getCartProducts()
     
    }
}
</script>

<style>
  .container{
    display: grid;
    grid-template-rows: 60px ;
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
  .item {
    align-content: center;
    justify-content: center;
  }
</style>