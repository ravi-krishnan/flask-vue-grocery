<template>
  <div>
    <NavBar></NavBar>
    <h3>{{ name }}</h3>
    <p>Quantity: {{ quantity }}</p>
    <div>Price : ₹{{ price }}</div>
    <p>Category : {{ category }}</p>
    <a  class="btn btn-success btn-sm" @click="toggleInputFn">Buy</a>
      <div v-if="toggleInput">
          <input type="number" v-model.number="count" placeholder="enter the number of products required">
          <a  class="btn btn-success btn-sm" @click="addtoCart(count,price,name,current_user)">Add to Cart</a>
      </div>
    <br> <br>
    <p></p>
    <div v-if=sm >
      <button data-toggle="modal" data-target="#deleteModal" class="btn btn-danger">Delete</button>
      <router-link :to="`/products/edit/${id}`" class="btn btn-warning">Edit</router-link>
    </div>
    




    <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
                <div class="modal-dialog" role="document">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title" id="deleteModalLabel">Delete Product?</h5>
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                      </button>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                      <form>
                        <input @click="this.deleteProduct" class="btn btn-danger" type="submit" value="Delete">
                      </form>
                    </div>
                  </div>
                </div>
              </div>
  </div>
</template>

<script>
import NavBar from '../NavBar'
export default {
    props: {
        id: {
          type: [Number, String],
          required: true
        }
    },
    components:{
      NavBar: NavBar
    },
    data () {
        return{
            admin:false,
            sm:false,
            message : 'Product Page of ',
            name:'',
            quantity:null,
            price:null,
            category :null,
            count:null,
            toggleInput:false,
            current_user:null
        }
        
    },
    methods:{
      toggleInputFn() {
      this.toggleInput = !this.toggleInput
    },
      loadcurrentuser() {
        const token = this.$getCookie('access_token')
        this.sm=this.$isSM(token)
        this.current_user=this.$current_user(token)
      },
      deleteProduct() {
        const token =this.$getCookie('access_token')
        fetch(`http://localhost:5000/products/${this.id}`, {
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
          window.alert('ERRROR'+err)
        })
      },
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
          this.category=data.category_name
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
    },
    created () {
      this.loadProduct()
      this.loadcurrentuser()
    }
}
</script>

<style>

</style>