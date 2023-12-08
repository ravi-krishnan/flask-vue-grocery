<template>
  <div class="body">
    <NavBar />
    
    <form class="center">
        <h2>Store Manager Signup</h2>
        <div class="form-group">
            <label for="un">Username</label>
            <input v-model="username" type="text" class="form-control" id="un" placeholder="Enter your username">
        </div>
        <div class="form-group">
            <label for="em">Email</label>
            <input v-model="email" type="email" class="form-control" id="em" placeholder="Enter your Email">
        </div>
        <div class="form-group">
            <label for="pass">Password</label>
            <input v-model="password" type="password" class="form-control" id="pass" placeholder="Enter your password">
        </div>
        <div class="form-group">
            <button  @click=submitSM class="form-control btn btn-lg btn-primary">Submit</button>
        </div>
        <br>
        <router-link to="/register">Click here to signup as a user</router-link>
    </form>

    

  </div>
</template>

<script>
import NavBar from '../components/NavBar'
export default {
    data () {
        return {
            username: null,
            password : null,
            email : null
        }
    },
    components:{
        NavBar: NavBar
    },
    methods:{
        submitSM () {
            fetch('http://localhost:5000/admin/sm/requests',{
                method: 'POST',
                headers: {
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({
                    username : this.username,
                    email : this.email,
                    password : this.password,
                })
            })
            .then( async resp=>{
                    if (!resp.ok){
                        const jresp =  await resp.json()
                        console.log(jresp)
                        throw new Error(jresp.message || 'Invalid Response')
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
            .catch(err =>{
                this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
            })
        }
    }

}
</script>

<style>

</style>