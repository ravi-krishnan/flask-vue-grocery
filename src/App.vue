<template>
  <div id="app">
    <router-view/>
    <notifications group="success"  position="top center"/>
    <notifications group="fail"   position="top center"/>
    <notifications group="warning"  position="top center"/>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
.center{
  
    padding: 5px;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 30%;
    margin: auto;
    transform: translate(-50%,-50%);  
}
body{
  background-color: rgb(214, 214, 219);
}
.card{
  border-radius: 30px;
  width: 96%;
}
.col-sm-3{
  margin-top: 3px;
  margin-bottom: 3px;
}
</style>
