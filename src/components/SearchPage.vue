<template>
    <div>
        <NavBar />
        <div class="dropdown">
            <button style="position: absolute; left: 20%; margin-top: 1em;"  class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Filter
            </button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <div   v-for="category in this.get_categories" :key="category.name" >
                    <router-link :to="`/categories/${category.id}`">
                    {{ category.name }}
                    </router-link> 
                </div>
                
            </div>
        </div>
        <div style="position: absolute;top: 50%;left: 50%; transform: translate(-50%,-50%);" v-if="searchData.message">{{searchData.message}}</div>
        <div style="margin-top: 60px;"></div>
        <div class="my-3"  v-for="data in searchData" :key="data.id">
            <router-link :to="`/products/${data.id}`">{{ data.name }}</router-link>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
    data () {
        return {
            results : []
        }
    },
    components: {
        NavBar:NavBar
    },
    computed :{
        searchData() {
            return this.$store.state.results
    },
        get_categories() {
                return this.$store.getters.get_categories
    }
  }
}
</script>

<style>

</style>