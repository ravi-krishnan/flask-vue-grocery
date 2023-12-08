<template>
    <div>
        <NavBar></NavBar>
    <div class="container">
        <div class="row" style="padding-bottom: 10px;">
            <div class="col">
                <h4> Product Sales</h4>
                <img :src="ploturl" alt="Plot-Chart" >
            </div>
            <div class="col">
                <h4>Product-Category Distribution</h4>
                <img :src="pyurl" alt="Pie-Chart" >
            </div>
        </div>
        
       
    </div>    
    <div class="row hihi">
        <div class="col-sm-2" style="margin-left: 30%;">Create Product  <router-link to="/products/add"><button class="btn btn-lg btn-white">+</button></router-link></div>
        <div class="col-sm-3">Create Category   <router-link to="/categories/add"><button class="btn btn-lg btn-white">+</button></router-link></div>
    </div>
    <div class="row">
        <div class="col" style="width: 97%;">
            <button class="btn btn-primary" @click="exportCSV">Export CSV</button><span v-if="isWaiting">Waiting...</span>
        </div>
        
      
    </div>
    </div>
  
</template>

<script>
import NavBar from './NavBar.vue'
export default {
    data(){
        return{
            pyurl:'',
            ploturl:'',
            isWaiting:false,
        }
    },
    components:{
        NavBar
    },
    methods:{
        exportCSV(){
      this.isWaiting= true
      fetch('http://localhost:5000/sm/download-csv', { 
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
          console.log(data)
          const taskId=data['task_id']
          const intv= setInterval(async () =>{
            const csv_res= await fetch(`http://localhost:5000/sm/csv/${taskId}`)
            if (csv_res.ok){
              clearInterval(intv)
              window.alert('Ready to Download')
              window.location.href = `http://localhost:5000/sm/csv/${taskId}`
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
        async plot () {
            const response=await fetch('http://localhost:5000/sm/chart/recent_buy')
            const blob = await response.blob()
            const data_url=URL.createObjectURL(blob)
            this.ploturl=data_url
            
        },
        async pie () {
            const response=await fetch('http://localhost:5000/sm/chart/pie')
            const blob = await response.blob()
            const data_url=URL.createObjectURL(blob)
            this.pyurl=data_url
            
        }
    },
    mounted(){
        this.plot()
        this.pie()
    }
}
</script>

<style scoped>
.hihi{
    margin-top: 30px;
}
.container{
    border: inset;
    width: 100%;
    height:max-content

}
img{
    width: 400px;
}
</style>