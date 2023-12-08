<!-- works with fetch call having mode=cors -->

<template>
    <div class="body">
        
        <NavBar />
        
    <div class="register">
        <h2 class="mb-5">Register Page</h2>
        
        <form class="form">
            <div class="form-group">
                <label for="us">Username</label>
                <input v-model=username  class="form-control" type="text" id="us" placeholder="Enter your Username">
            </div>
            <div class="form-group">
                <label for="em">Email</label>
                <input v-model=email class="form-control" type="email" id="em" placeholder="Enter your Email">
            </div>
            <div class="form-group">
                <label for="ps">Password</label>
                <input v-model=password class="form-control" type="password" id="ps" placeholder="Enter your Password">
            </div>
            <div class="form-group">
                <input @click=RegisterUser class="form-control btn btn-primary" type="submit" value="Submit">
            </div>
        </form>
        <router-link to="/login">Click here for registerd users</router-link><br>
        <router-link to="/sm">Click here to signup as a Store Manager</router-link>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar'
export default {
    data () {
        return {
            username : '',
            password : '',
            email : ''
        }
    },
    components: {
        NavBar : NavBar
    },
    methods : {
        RegisterUser () {
            // console.log(this.username)
            // console.log(this.email)
            // console.log(this.password)
            fetch('http://localhost:5000/auth/register', {
                method : 'POST',
                
                headers: {
                    'Content-Type': 'application/json',

                },
                body: JSON.stringify({
                    username : this.username,
                    email : this.email,
                    password : this.password
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
                    this.$router.push('/login')
                })
                .catch(err =>{
                    this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
                })
                    // window.alert(err)
                })
            }
        }
    }

</script>

<style>
.register{
    padding: 5px;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 30%;
    margin: auto;
    transform: translate(-50%,-50%);  
}
</style>