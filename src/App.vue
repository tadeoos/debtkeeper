<template>
  <div id="app">
    <DebtKeeper/>
  </div>
</template>

<script>
import DebtKeeper from './components/DebtKeeper.vue'

export default {
  name: 'app',
  components: {
    DebtKeeper
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
  body {
    background-color: #eee;
  }
</style>
