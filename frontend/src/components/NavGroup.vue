<template>
  <div class="btn-group nav-dk">
    <div class="dropdown">
      <div class="btn-group">
        <router-link :to="{name: 'Ledger'}" exact
                     tag="button"
                     :class="ledgerClass">
          Ledger
        </router-link>
        <a href="#" class="dropdown-toggle" :class="ledgerClass" tabindex="0" v-if="activeEl === 'ledger'">
          <i class="icon icon-caret"></i>
        </a>
        <!-- menu component -->
        <ul class="menu">
          <li class="menu-item">
            <label class="form-checkbox">
              <input v-model="debtsFilter" type="checkbox">
              <i class="form-icon"></i> Debts
            </label>
          </li>
          <li class="menu-item">
            <label class="form-checkbox">
              <input v-model="loansFilter" type="checkbox">
              <i class="form-icon"></i> Loans
            </label>
          </li>
          <li class="menu-item">
            <label class="form-checkbox">
              <input v-model="unresolvedFilter" type="checkbox">
              <i class="form-icon"></i> Unresolved
            </label>
          </li>
          <li class="menu-item">
            <label class="form-checkbox">
              <input v-model="resolvedFilter" type="checkbox">
              <i class="form-icon"></i> Resolved
            </label>
          </li>
        </ul>
      </div>
    </div>
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
      },
      debtsFilter: {
        get() {
          return this.$store.state.ledgerFilters.debt;
        },
        set(value) {
          if (value == false && this.loansFilter == false) {
            this.loansFilter = true;
          }
          this.$store.dispatch('filter', {atr: 'debt',val: value});
        }
      },
      loansFilter: {
        get() {
          return this.$store.state.ledgerFilters.loan;
        },
        set(value) {
          if (value == false && this.debtsFilter == false){
            this.debtsFilter = true;
          }
          this.$store.dispatch('filter', {atr: 'loan',val: value});
        }
      },
      resolvedFilter: {
        get() {
          return this.$store.state.ledgerFilters.resolved;
        },
        set(value) {
          if (value == false && this.unresolvedFilter == false) {
            this.unresolvedFilter = true;
          }
          this.$store.dispatch('filter', {atr: 'resolved',val: value});
        }
      },
      unresolvedFilter: {
        get() {
          return this.$store.state.ledgerFilters.unresolved;
        },
        set(value) {
          if (value == false && this.resolvedFilter == false) {
            this.resolvedFilter = true;
          }
          this.$store.dispatch('filter', {atr: 'unresolved',val: value});
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
  .filter {
    margin-left: -0.1em;
    border-bottom-right-radius: .1rem;
    border-top-right-radius: .1rem;
    color: #5755D9;
  }
</style>
