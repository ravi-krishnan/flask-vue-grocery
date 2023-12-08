<template>
  <div>
    <NavBar></NavBar>
    <div class="container">
        <div class="row" style="padding-bottom: 20px;">
            <div class="col">
                <h4>Users Status</h4>
                <img :src="active_url" alt="active_plot">
            </div>   
            <div class="col">
                <h4>Checkout Record</h4>
                <img :src="best_url" alt="best_plot">
            </div>   
        </div>
        

    </div>


  </div>
</template>

<script>
import NavBar from './NavBar.vue'
export default {
    data(){
        return {
            active_url:'',
            best_url:''
        }
    },
    components:{
        NavBar
    },
    methods:{
        async active_inactive(){
            const response= await fetch('http://localhost:5000/admin/chart/active')
            // if (response.json().message==='No active users for a while now'){
            //     this.active_url='mimi'
            // }
            const blob = await response.blob()
            const url = URL.createObjectURL(blob)
            this.active_url=url

                

        },
        async best_users(){
            const response= await fetch('http://localhost:5000/admin/chart/best')
            const blob = await response.blob()
            const url = URL.createObjectURL(blob)
            this.best_url=url

        }
    },
    created(){
        this.active_inactive()
        this.best_users()
    }
}
</script >

<style scoped>
.container{
    border: inset;
    width: 100%;
    height: max-content;
}
img{
    width: 500px;
}
</style>