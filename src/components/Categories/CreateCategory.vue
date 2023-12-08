<template>
  <div class="create">
    <NavBar />
    
    <form class="center">
        <h4 class="my-5">Create new Category</h4>
      <div class="form-group">
        <label for="Name">Name</label>
        <input v-model="name" class="form-control" type="text" name="Name" id="Name" placeholder="Enter Name of the Category">
      </div>
      <input v-if="this.sm"  @click=CreateCategory type="button" value="Request creation">
      <input class="btn btn-primary form-control" v-if="this.admin" @click=CreateCategory type="button" value="Create">
    </form>
</div>
</template>

<script>
import Vue from 'vue';
import NavBar from '../NavBar.vue'
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
            name :'',
            admin:false,
            sm:false
        }
    },
    components :{
        NavBar: NavBar
    },
    methods:{
        CreateCategory () {
            const token = this.$getCookie('access_token')
      
            fetch('http://localhost:5000/categories/', {
                method : 'POST',
                headers :{
                'Content-Type' : 'application/json',
                'Authorization' : `Bearer ${token}`
                },
                body:JSON.stringify({
                    name:this.name
                })
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
                this.$notify({
                    group: 'success',
                    type: 'success',
                    text: data.message,
            })
                
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
            is_sm(){
                const token = this.$getCookie('access_token')
                this.sm= this.$isSM(token)
            },
            is_admin(){
                const token = this.$getCookie('access_token')
                this.admin= this.$isAdmin(token)
            }
    },
    mounted(){
        this.is_admin()
        this.is_sm()
    }
        
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