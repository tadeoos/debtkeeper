<template>
  <div class="container">
    <div class="columns">
      <div class="column col-lg-12 col-4 col-mx-auto">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">
              <h5>About DebtKeeper</h5>
            </div>
            <div class="divider"></div>
          </div>
          <div class="panel-nav">
            <!-- navigation components: tabs, breadcrumbs or pagination -->
          </div>
          <div class="panel-body">
            <!-- contents -->
            <p>
              This web app helps you keep track of anything that you loaned or borrowed.
            </p>
            <p>
              You can save it on your mobile device and use it as any other regular app.
            </p>
            <p>
              It was created by <a href="https://tadek.tele.com.pl">Tadek Teleżyński</a>.
            </p>
          </div>
          <div class="panel-footer">
            <router-link :to="{name: 'Home'}" exact>
              <i class="icon icon-back"></i>
            </router-link>
            <!-- buttons or inputs -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "AboutPage"
  }
</script>

<style scoped>
  .panel{
    background: #ffffff;
  }
</style>
