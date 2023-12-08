<template>
    <div>
        <NavBar></NavBar>
        <h3>Edit Category</h3>
        <form class="center">
      <div class="form-group">
        <label for="Name">Name</label>
        <input v-model="name" class="form-control" type="text" name="Name" id="Name" placeholder="Enter Name of the Category">
      </div>
      <input v-if="this.sm"  @click=UpdateCategory type="button" value="Request edit">
      <input class="btn btn-primary form-control"  v-if="this.admin" @click=UpdateCategory type="button" value="Edit">
    </form>
    </div>
</template>

<script>
import Vue from 'vue';
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
            name :'',
            products : [],
            admin:false,
            sm:false
        }
    },
    components :{
        NavBar: NavBar
    },
    props: {
        id: {
        type: [Number, String],
        required: true
        }
    },
    methods:{
        // getAllProducts(){
        //     fetch(`http://localhost:5000/categories/${this.id}/products`,{
        //         method: 'GET',
        //         headers :{
        //             'Content-Type':'application/json'
        //         }
        //     })
        //     .then(res =>res.json())
        //     .then(data => {
                
        //         this.products.push(...data)
        //         console.log(this.products)
        //     })
        //     .catch(err => console.log(err))
        // },


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
          console.log(data)
          this.name=data.name
        })
        .catch( err => {
          console.log(err)
          window.alert('ERRROR'+err)
        })
      },
      UpdateCategory() {
        const token = this.$getCookie('access_token')
        fetch(`http://localhost:5000/categories/${this.id}`, {
          method :'PUT',
          headers : {
            'Content-Type' : 'application/json',
            'Authorization' : `Bearer ${token}`
          },
          body : JSON.stringify({
            name : this.name,
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
      is_sm(){
          const token = this.$getCookie('access_token')
          this.sm= this.$isSM(token)
      },
      is_admin(){
          const token = this.$getCookie('access_token')
          this.admin= this.$isAdmin(token)
      },
    },
    created (){
        this.loadCategory()
        this.is_admin()
        this.is_sm()
        // this.getAllProducts()
    },
    // computed :{
    //     AfterUpdate(){
    //         return this.name
    //     }
    // },
    // watch:{
    //     AfterUpdate(name){
    //         console.log(`value changed to ${name}`)
    //         console.log(this.products.length)
    //         for ( let i=0; i<this.products.length;i++){
    //             this.products[i].category_name=this.name
    //             console.log(this.products[i].category_name)
    //         }
    //     }
    // }

}
</script>

<style>
    .center{
    /* border: 2px solid black; */
    padding: 5px;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 30%;
    margin: auto;
    transform: translate(-50%,-50%);  
    }
</style>