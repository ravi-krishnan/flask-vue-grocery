<template>
  <div>
    <NavBar></NavBar>
    <div>
      <p>{{ userDetails.user }}</p>
      <p>{{ userDetails.email }}</p>
      

      <div v-if="userDetails.sm">
        <button class="btn btn-primary" @click="exportCSV">Export CSV</button><span v-if="isWaiting">Waiting...</span>
      </div>

    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'
export default {
  data(){
    return {
      isWaiting:false,
      userDetails:[],
      user:''
    }
  },
  components:{
        NavBar
    },
  methods:{
    exportCSV(){
      this.isWaiting= true
      fetch('http://localhost:5000/download-csv', { 
          method: 'GET',
          headers: {
            // 'Content-Type':'application/json',
            // 'Authorization': `Bearer ${token}`,
            
        }})
        .then(async resp => {
          if (!resp.ok){
            // this.isWaiting= false
            console.log(resp)
            const jsonresponse=await resp.json()
            throw new Error(jsonresponse.message||'Invalid Response')
          }
          // console.log(resp)
          return resp.json()
        })
        .then(data =>{ 
          // console.log(data['task_id'])
          const taskId=data['task_id']
          const intv= setInterval(async () =>{
            const csv_res= await fetch(`http://localhost:5000/csv/${taskId}`)
            if (csv_res.ok){
              clearInterval(intv)
              window.alert('Ready to Download')
              window.location.href = `http://localhost:5000/csv/${taskId}`
              this.isWaiting= false
            }
            else{
              console.log('eroor')
              clearInterval(intv)
              // console.log('2')
              this.isWaiting= false
            }
          },1000)})
        .catch(err => console.log('Error: '+err.message))
    },
    getuserdetails(){
      fetch(`http://localhost:5000/users/${this.user}/account`,{
        method:'GET',
        headers:{
          'Content-Type':'application/json'
        }
      })
      .then(resp => {
        console.log(resp)
        if (!resp.ok){
          const resp_json = resp.json()
          throw new Error(resp.json.message || 'Invalid Response')
        }
        return resp.json()
      })
      .then(data =>{
        console.log(data)
        this.userDetails=data
      })
      .catch(err=>{
        this.$notify({
                    group: 'fail',
                    type: 'error',
                    text: err,
            })
        console.log(err)
      })
    },
    current_user(){
      const token = this.$getCookie('access_token')
      this.user=this.$current_user(token)
    },
  },
  computed:{
    // is_sm(){
    //   const token = this.$getCookie('access_token')
    //   return this.$isSM(token)
    // }

  },
  created(){
    
    this.current_user()
    
  },
  mounted(){
    this.getuserdetails()
  }
}
</script>

<style>

</style>