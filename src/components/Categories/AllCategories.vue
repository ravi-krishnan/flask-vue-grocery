<template>
    <div>
        <NavBar/>
          <h3 style="margin-top: 40px; margin-bottom: 40px;" >Categories</h3>
            <!-- <p v-for="category in categories" :key="category.id"> -->
              <p v-for="category in getAllCategoriesVUEX" :key="category.id">
                <router-link :to="`/categories/${category.id}`">
                    {{ category.name }}
                </router-link> 
            </p>
        
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
    data () {
        return {
            categories : []
        }
    },
    components:{
        NavBar
    },
    methods: {
    // getAllCategories () {
    //   // const token = this.$getCookie('access_token') {
    //       fetch('http://localhost:5000/categories/', { 
    //       method: 'GET',
    //       headers: {
    //         'Content-Type':'application/json',
    //         // 'Authorization': `Bearer ${token}`,
            
    //     }})
    //     .then(async resp => {
    //       if (!resp.ok){
    //         const jsonresponse=await resp.json()
    //         throw new Error(jsonresponse.message||'Invalid Response')
    //       }
    //       return resp.json()
    //     })
    //     .then(data =>{ 
    //       console.log(data)
    //       this.categories.push(...data)
    //     })
    //     .catch(err => console.log('Error: ' + err.message))

    //   },
    },
    //rewrite the code
  created () {
    this.$store.dispatch('fetch_categories')
    // this.getAllCategories()
  },
  mounted(){
    
  },
  computed:{
    getAllCategoriesVUEX(){
      return this.$store.getters.get_categories
    }
  }
}
</script>

<style>

</style>