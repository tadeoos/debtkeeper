<template lang="html">
  <div class="container">
    <div class="columns">
      <div class="column col-lg-12 col-4 col-mx-auto">
        <NavGroup active-el=""/>
        <form>
          <div class="form-group">
            <label class="form-label" for="id_username">Username</label>
            <input v-model="username" class="form-input" type="text" id="id_username" placeholder="Username"
                   autofocus="autofocus"
                   maxlength="150"
                   :class="{ 'is-error': error }">
            <label class="form-label" for="id_password">Password</label>
            <input v-model="password" class="form-input" type="password" id="id_password" placeholder="Password"
                   :class="{ 'is-error': error }">
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
  import NavGroup from "./NavGroup";

  export default {
    name: "LoginPage",
    components: {
      NavGroup
    },
    data() {
      return {
        username: '',
        password: '',
        errorMsg: '',
        error: false,
      }
    },
    computed: {
      formData() {
        let bodyFormData = new FormData();
        bodyFormData.set('username', this.username);
        bodyFormData.set('password', this.password);
        return bodyFormData
      }
    },
    methods: {
      valdiate() {
        if (!self.username || !self.password) {
          this.error = true;
        }
        else {
          this.error = false;
        }
      },
      authenticate() {
        this.valdiate();
        if (self.error){
          return
        }
        this.$store.dispatch('login', this.formData)
            .then(() => this.$router.push('/ledger'))
      },
      register() {
        this.valdiate();
        if (self.error){
          return
        }
        this.$store.dispatch('register', this.formData)
            .then(() => this.$store.dispatch('login', this.formData))
            .catch((error) => {
              console.log(error)
            })
      }
    },
    mounted() {
      EventBus.$on('failedRegistering', (msg) => {
        this.errorMsg = msg
      });
      EventBus.$on('failedAuthentication', (msg) => {
        this.errorMsg = msg
      });
    },
    beforeDestroy() {
      EventBus.$off('failedRegistering');
      EventBus.$off('failedAuthentication');
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
