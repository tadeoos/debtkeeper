<template>
  <div class="btn-group nav-dk">
    <router-link :to="{name: 'Ledger'}" exact
                 tag="button"
                 :class="ledgerClass">
      Ledger
    </router-link>
    <router-link :to="{name: 'AddItem'}" exact
                 tag="button"
                 :class="addClass">
      Add item
    </router-link>
    <router-link :to="{name: 'About'}" exact
                 tag="button"
                 :class="aboutClass">
      About
    </router-link>
    <button class="btn btn-sm" v-if="accountAction" @click="logout()">
      Logout
    </button>
  </div>
</template>

<script>
  export default {
    name: "NavGroup",
    props: {
      activeEl: {
        type: String,
        default: 'menu'
      }
    },
    computed: {
      accountAction() {
        if (this.$store.getters.isAuthenticated) {
          return 'Logout'
        } else {
          return false
        }
      },
      addClass() {
        return {
          active: this.activeEl === 'add',
          btn: true,
          'btn-sm': true
        }
      },
      ledgerClass() {
        return {
          active: this.activeEl === 'ledger',
          btn: true,
          'btn-sm': true
        }
      },
      aboutClass() {
        return {
          active: this.activeEl === 'about',
          btn: true,
          'btn-sm': true
        }
      }
    },
    methods: {
      logout: function () {
        this.$store.dispatch('logout');
        this.$router.replace({name: "Home"});
      }
    },
  }
</script>

<style scoped>
  .nav-dk {
    margin-bottom: 1em;
  }
</style>
