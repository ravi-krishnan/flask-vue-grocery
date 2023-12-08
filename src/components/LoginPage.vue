<!-- everything works fine -->
<!-- except it takes one reload before passing another login paramaets -->
<template>
  <div>
    <NavBar />
    
    <div class="center">
        <h2 class="my-5">Login Page </h2>
    <form >
        <div class="form-group">
            <label for="un">Username</label>
            <input v-model="username" type="text" class="form-control" id="un" placeholder="Enter your username">
        </div>
        <div class="form-group">
            <label for="pass">Password</label>
            <input v-model="password" type="password" class="form-control" id="pass" placeholder="Enter your password">
        </div>
        <div class="form-group">
            <button @click=submitForm class="form-control btn btn-lg btn-primary">Submit</button>
        </div>
    </form>
    <footer>
        <router-link to="/register">Click here to signup</router-link>
    </footer>
</div>
    


  </div>
</template>

<script>
import NavBar from '@/components/NavBar'
export default {
    data() {
        return {
            
            username: '',
            password: '',
            body:{}
        }
    },
    components : {
        NavBar : NavBar
    },
    methods:{
        // fn to take values and store and call fetch
        // fetch
        // 
        submitForm(){

            try{
                // const data={
                //         username:this.username,
                //         password:this.password,
                //     }
                // console.log(this.body)
                fetch('http://localhost:5000/auth/login',{
                    method:'POST',
                    headers: {
                        'Content-Type':'application/json'
                    },
                    // credentials:'include',
                    body:JSON.stringify({
                        username: this.username,
                        password: this.password,
                    })
                })
                .then(async resp => {
                    if (!resp.ok){
                        const jresponse= await resp.json()
                        console.log(jresponse)
                        throw new Error(jresponse.message)
                    }
                    return resp.json()
                })
                .then(
                    data => {
                        console.log(data)
                        console.log(data.message)
                        const access_token=data.token.access
                        const refresh_token=data.token.refresh
                        document.cookie=`access_token=${access_token}; Path=/ `
                        document.cookie=`refresh_token=${refresh_token}; Path=/ `
                        this.$notify({
                            group: 'success',
                            type: 'success',
                            text: data.message,
                        })
                        this.$store.commit('update_logout',true)
                        this.$router.push('/')
                        
                    }
                )
                .catch(
                    err =>{
                        console.log(err)
                        this.$notify({
                            group: 'fail',
                            type:"error",
                            text: err,
                    })
                        // window.alert(err.message)
                    }
                )
            }
            catch (err){
                console.log(err)
            }
            // fetch('http://localhost:5000/auth/set-cookie', {
            //     method: 'GET',
            //     credentials: 'include',
            //     })
            //     .then(response => {
                    
            //         console.log(response)
            //     })
            //     .then( data => {
            //         console.log(data)
            //     })
            //     .catch(error => {
            //         // Handle the error
            //         console.log(error)
            //     });





        }
    }

    }
</script>

<style >
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
.body{
    color: rgb(71, 45, 13);
}

</style>