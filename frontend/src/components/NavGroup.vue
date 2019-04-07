<template>
  <div class="btn-group nav-dk">
    <router-link :to="{name: 'Home'}" exact
                 tag="button"
                 :class="menuClass">
      Menu
    </router-link>
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
      menuClass() {
        return {
          active: this.activeEl === 'menu',
          btn: true,
          'btn-sm': true
        }
      }
    }
  }
</script>

<style scoped>
  .nav-dk {
    margin-bottom: 1em;
  }
</style>
