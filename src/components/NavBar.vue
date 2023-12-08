<!-- logout fn works.. but the logout btn cant be hided -->
<template>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-steel bg-steel">
        <a class="navbar-brand" href="#">Shopy</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <router-link class="nav-item nav-link" to="/">Home</router-link>
                <router-link v-if="admin" class="nav-item nav-link ml-1" to="/admin/">Dashboard</router-link>
                <router-link v-if="sm" class="nav-item nav-link ml-1" to="/sm/dashboard">Dashboard</router-link>
                <router-link to="/categories" class="nav-item nav-link ml-1">Categories</router-link>
                <!-- <a class="nav-item nav-link active" href="#">Home <span class="sr-only">(current)</span></a> -->
                <!-- <a class="nav-item nav-link" href="#">Features</a>
                <a class="nav-item nav-link" href="#">Pricing</a>
                <a class="nav-item nav-link disabled" href="#">Disabled</a> -->
            </div>
            <!-- <div class="navbar-nav mx-auto">
                <a class="nav-item nav-link" href="#">Login</a>
            </div> -->
            <div class="navbar-nav ml-auto">
                <form  style="margin-top: 5px;" class="mr-3">
                    <input v-model=query type="text" placeholder="Search for products">
                    <!-- <router-link @click="searchQuery" class="mr-3" to="/search">Search </router-link> -->
                    <input class="btn btn-primary btn-sm" @click="searchQuery" type="submit">
                </form>
                <li v-if="admin || sm" class="nav-item dropdown">
                    <a  class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <router-link style="margin-top: -8px;text-decoration: none;" to="#">Create</router-link>
                    </a>
                    <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                    <a v-if="sm" class="dropdown-item"><router-link to="/products/add">Product</router-link></a>
                    <a v-if="admin || sm" class="dropdown-item" href="#"><router-link to="/categories/add">Category</router-link></a>
                    </div>
                </li>
                <li class="nav-item">
                    <router-link v-if="user" class="nav-item nav-link" to="/cart">Cart </router-link>
                </li>
<!--                 
                <li class="nav-item">
                    <router-link  v-if="user &&!admin&&!sm" class="mr-3 " to="/account">Account</router-link>
                </li> -->
                
                <li class="nav-item">
                    <router-link class="nav-item nav-link " to="/login">Login</router-link>
                </li>
                <!-- <router-link class="mr-3" to="/register">Register </router-link> -->
                
                <a class="nav-item nav-link" v-if=this.$store.getters.get_logout @click=LogoutUser href="#">Logout</a>
                
                

            </div>
        </div>
    </nav>
    </div>
</template>
<script>
import Cookies from 'js-cookie';
export default {
    name: 'NavBar',
    data (){
        return {
            query:'',
            results:[],
            admin:'',
            sm:'',
            user:''
        }
    },
    methods: {
        searchQuery(){
            if (this.query==''){
                // this.$router.push('/')
                this.$notify({
                    group: 'warning',
                    type: 'warn',
                    text: 'Blank Search Field found'
                
                 })
                this.$router.push('/')
            }
            else{
                this.$router.push('/search')
                fetch('http://localhost:5000/products/search',{
                method:'POST',
                headers: {
                    'Content-Type':'application/json'
                },
                body:JSON.stringify({
                    query : this.query
                })
                })
                .then(async res => {
                    if (!res.ok){
                        const jres =await res.json()
                        throw new Error(jres.message || 'Invalid Response')
                    }
                    return res.json() 
                })
                .then(data => {
                    // console.log(data)
                    console.log(data)
                    // this.results=data
                    // this.results.push(...data)
                    this.$store.commit('setSearchResults',data)
                })
                .catch(err => console.log(err))
            }
            

        },
        current_user(){
            const token = this.$getCookie('access_token')
            this.user=this.$current_user(token)
            this.sm=this.$isSM(token)
            this.admin=this.$isAdmin(token)
        },
        LogoutUser () {
            console.log('Logout Fn')
            const token = this.$getCookie('access_token')
            console.log(token)
            fetch('http://localhost:5000/auth/logout', {
                method : 'GET',
                headers :{
                    'Content-Type' : 'application/json',
                    'Authorization' : `Bearer ${token}`
                    
                },
            })
            .then(async res => {
                if (!res.ok){
                    const jres =res.json()
                    throw new Error(jres.message || 'Invalid Response')
                }
                return res.json() 
            })
            .then(data => {
                // console.log(data)
                console.log(data)
                Cookies.set('access_token','',{expires:0})
                Cookies.set('refresh_token','',{expires:0})
                // this.$store.commit("take_response",data)
                this.$notify({
                    group: 'success',
                    type: 'success',
                    text: data.message
                
            })
                this.$store.commit('update_logout',false)
                this.$router.push('/')
                setTimeout(()=>window.location.reload(),1000)
                
                
            })
            .catch(err => {
                this.$notify({
                    group: 'fail',
                    type: 'fail',
                    text: err,
            })
                // window.alert(err)
            })
        },
    },
    created(){
        this.current_user()
    }

}
</script>

<style>

</style>