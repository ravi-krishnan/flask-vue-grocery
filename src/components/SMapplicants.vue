<template>
  <div>
        <NavBar></NavBar>
        <div class="container">
            <h3 v-if="applicants.length==0" ></h3>
            <h3 v-if="applicants.length>0" >Store Manager Applications</h3>
            <div v-for="applicant in applicants" :key=applicant.username>
                {{applicant.username}}   {{applicant.email}} 
                <br>
                <button @click=approveSM(applicant.username)  class="btn btn-success">Approve</button>
                <button @click=disapproveSM(applicant.username) class="btn btn-danger">Disapprove</button>
            </div>   

        </div>
    </div>
</template>

<script>
import NavBar from './NavBar.vue'
export default {
data () {
    return {
        msg:'Hi',
        applicants:[],
    }
},
components:{
    NavBar
},
methods: {
    getallSubmissions() {
        const token =this.$getCookie('access_token')
        fetch('http://localhost:5000/admin/sm/requests', {
            method: 'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${token}`
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
            this.applicants.push(...data)
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
    disapproveSM(un) {
        const token = this.$getCookie('access_token')
        fetch('http://localhost:5000/admin/sm/disapprove', {
            method: 'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${token}`
            },
            body: JSON.stringify({
                username : un,
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
    approveSM (un) {
        const token = this.$getCookie('access_token')
        fetch('http://localhost:5000/admin/sm/approve', {
            method: 'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization':`Bearer ${token}`
            },
            body: JSON.stringify({
                username : un,
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
},
created () {
    this.getallSubmissions()
}
}
</script>

<style>

</style>