<template>
  <div class="container">
    <div class="columns">
      <div class="column col-6 col-sm-12 col-mx-auto">
        <div class="panel">
          <div class="panel-header">
            <NavGroup active-el="about"/>
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
            <p>This is a <span class="label label-warning">BETA</span> version.</p>
            <p> There is a
              possibility that some of your data will be lost, but I'll do my best to avoid it.</p>
            <p>
              You can save it on your mobile device and use it as it was a normal mobile app.
            </p>
            <p>
              It was created by <a href="https://tadek.tele.com.pl">Tadek Teleżyński</a>.
            </p>
          </div>
          <div class="panel-footer">
            <!-- buttons or inputs -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import NavGroup from "./NavGroup";

  export default {
    name: "AboutPage",
    components: {
      NavGroup
    }
  }
</script>

<style scoped>
  .panel{
    background: #ffffff;
    margin-top: 1em;
  }
</style>
