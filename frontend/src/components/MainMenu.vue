<template>
  <div class="container">
    <div class="columns">
      <div class="column col-lg-12 col-4 col-mx-auto">
        <ul class="menu">
          <!-- menu header text -->
          <li class="divider" data-content="MENU">
          </li>
          <!-- menu item standard -->
          <li class="menu-item">
            <router-link :to="{name: 'Login'}" exact>
              Login
            </router-link>
          </li>
          <li class="menu-item">
            <router-link :to="{name: 'Ledger'}" exact>Ledger</router-link>
          </li>
          <li class="menu-item">
            <router-link :to="{name: 'Ledger'}" exact>Add item</router-link>
          </li>
          <li class="menu-item">
            <router-link :to="{name: 'About'}" exact>About</router-link>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "MainMenu"
  }
</script>

<style scoped>

</style>
