<template lang="html">
  <div class="container">
    <div class="columns">
      <div class="column col-lg-12 col-4 col-mx-auto">
        <div class="menu-link">
          <router-link :to="{name: 'Home'}" exact>
            <i class="icon icon-menu"></i>
          </router-link>
        </div>
        <form>
          <div class="form-group">
            <label class="form-label" for="id_username">Username</label>
            <input v-model="username" class="form-input" type="text" id="id_username" placeholder="Username"
                   autofocus="autofocus"
                   maxlength="150">
            <label class="form-label" for="id_password">Password</label>
            <input v-model="password" class="form-input" type="password" id="id_password" placeholder="Password">
          </div>
          <div class="btn-group btn-group-block">
            <button
                    @click.prevent="authenticate"
                    class="btn btn-primary input-group-btn"
                    type="submit">
              Log in
            </button>
            <button
                    @click.prevent="register"
                    class="btn input-group-btn"
                    type="submit">
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  import {EventBus} from '@/utils'
  export default {
    name: "LoginPage",
    data() {
      return {
        username: '',
        password: '',
        errorMsg: ''
      }
    },
    methods: {
      authenticate() {
        this.$store.dispatch('login', {username: this.username, password: this.password})
            .then(() => this.$router.push('/'))
      },
      register() {
        this.$store.dispatch('register', {username: this.username, password: this.password})
            .then(() => this.$router.push('/'))
      }
    },
    mounted() {
      EventBus.$on('failedRegistering', (msg) => {
        this.errorMsg = msg
      })
      EventBus.$on('failedAuthentication', (msg) => {
        this.errorMsg = msg
      })
    },
    beforeDestroy() {
      EventBus.$off('failedRegistering')
      EventBus.$off('failedAuthentication')
    }
  }
</script>

<style scoped>
.form-group {
  text-align: left;
}
.menu-link{
  margin-top: -50px;
  margin-bottom: 30px;
  text-align: left;
}
</style>
