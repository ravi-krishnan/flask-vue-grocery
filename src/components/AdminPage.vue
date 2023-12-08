<template>
    <div>
        <NavBar></NavBar>
        <router-link to="/dashboard/applicants">Store Manager Applications</router-link> <br>
        <router-link to="/admin/summary">Summary</router-link>
        <div class="container">

        <div class="category-applicants-1">
            <h3  v-if="create_categories.length>0">Category creation requests</h3>
            <div v-for="category in create_categories" :key=category.name>
                {{category.name}}
                <br>
                <button @click=approvecreateCategory(category.name)  class="btn btn-success">Approve</button>
                <button @click=disapprovecreateCategory(category.name) class="btn btn-danger">Disapprove</button>
            </div>   

        </div>
        <div class="category-applicants-2">
            <h3  v-if="edit_categories.length>0">Category editing requests</h3>
            <div v-for="category in edit_categories" :key=category.name>
                {{category.name}} to {{ category.new_name }} <br>
                <button @click=approveeditCategory(category.name,category.new_name)  class="btn btn-success">Approve</button>
                <button @click=disapproveeditCategory(category.name) class="btn btn-danger">Disapprove</button>
            </div>   

        </div>
        <div class="category-applicants-3">
            <h3 v-if="delete_categories.length>0">Category deletion requests</h3>
            <div v-for="category in delete_categories" :key=category.name>
                {{category.name}} <br>
                <button @click=approvedeleteCategory(category.name)  class="btn btn-success">Approve</button>
                <button @click=disapprovedeleteCategory(category.name) class="btn btn-danger">Disapprove</button>
            </div>   

        </div>
    </div>
    </div>
</template>

<script>
import NavBar from './NavBar.vue'
import Vue from 'vue';
export default {
    beforeRouteEnter(to,from,next){
        const token = Vue.prototype.$getCookie('access_token');
        if( !token || !Vue.prototype.$isAdmin(token)){
            window.alert('Forbidden route')
            next('/login')
        }
        else{
            next()
        }
    },
    data () {
        return {
            create_categories:[],
            edit_categories:[],
            delete_categories:[],
        }
    },
    components:{
        NavBar
    },
    methods:{
        getallcreateRequests() {
            fetch('http://localhost:5000/categories/requests/create', {
                method: 'GET',
                headers:{
                    'Content-Type':'application/json',
                }
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
                this.create_categories.push(...data)
            })
            .catch(err =>{
                this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
                // window.alert(err)
            })
        },
        getalleditRequests() {
            fetch('http://localhost:5000/categories/requests/edit', {
                method: 'GET',
                headers:{
                    'Content-Type':'application/json',
                }
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
                this.edit_categories.push(...data)
            })
            .catch(err =>{
                this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
                // window.alert(err)
            })
        },
        getalldeleteRequests() {
            fetch('http://localhost:5000/categories/requests/delete', {
                method: 'GET',
                headers:{
                    'Content-Type':'application/json',
                }
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
                this.delete_categories.push(...data)
            })
            .catch(err =>{
                this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
                // window.alert(err)
            })
        },
        approvecreateCategory (name) {
            const token = this.$getCookie('access_token')
            fetch('http://localhost:5000/categories/requests/create/approve', {
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${token}`
                },
                body: JSON.stringify({
                    name : name,
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
                })
        },

        disapprovecreateCategory(name) {
            const token = this.$getCookie('access_token')
            fetch('http://localhost:5000/categories/requests/create/disapprove', {
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${token}`
                },
                body: JSON.stringify({
                    name : name,
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
                })
        },
        approveeditCategory (name,new_name) {
            const token = this.$getCookie('access_token')
            fetch('http://localhost:5000/categories/requests/edit/approve', {
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${token}`
                },
                body: JSON.stringify({
                    name:name,
                    new_name : new_name,
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
                    // window.alert('ERRRRROR' + err)
                    this.$notify({
                        group: 'fail',
                        type: 'error',
                        text: err,
            })
                })
        },
        disapproveeditCategory(name) {
            const token = this.$getCookie('access_token')
            fetch('http://localhost:5000/categories/requests/edit/disapprove', {
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${token}`
                },
                body: JSON.stringify({
                    name : name,
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
                })
        },
        approvedeleteCategory (name) {
            const token = this.$getCookie('access_token')
            fetch('http://localhost:5000/categories/requests/delete/approve', {
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${token}`
                },
                body: JSON.stringify({
                    name : name,
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
                })
        },
        disapprovedeleteCategory(name) {
            const token = this.$getCookie('access_token')
            fetch('http://localhost:5000/categories/requests/delete/disapprove', {
                method: 'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${token}`
                },
                body: JSON.stringify({
                    name : name,
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
                location.reload()
                })
                .catch(err => {
                    console.log(err)
                    this.$notify({
                        group: 'fail',
                        type: 'error',
                        text: err,
            })
                })
        },


        
                
    },
    created () {
        this.getalleditRequests()
        this.getalldeleteRequests()
        this.getallcreateRequests()
    // mounted () {
    //     router.
    // }
}
}
</script>

<style scoped>
.container{
    display: grid;
    grid-template-rows: 70px ;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
}
.category-applicants-1{
    
    grid-area:1/1/-1/5 ;
}
.category-applicants-2{
    
    grid-area: 1/6/-1/10;
}
.category-applicants-3{
    
grid-area: 1/11/-1/-1;
}

</style>