<template>
  <div class="container">
    <div class="columns">
      <div class="debt-items column col-9 col-sm-12 col-mx-auto">
        <transition name="fade" mode="out-in">
          <div class="layered-paper" v-if="items.length" key="debts-exists">
            <NavGroup active-el="ledger"/>
            <div class="hide-sm">
              <table class="table table-striped">
                <thead>
                <tr>
                  <th @click="sort('kind')">Type <i v-if="currentSort === 'kind'"
                                                    v-bind:class="sortIconClass"></i>
                  </th>
                  <th @click="sort('who')">Who <i v-if="currentSort === 'who'"
                                                  v-bind:class="sortIconClass"></i>
                  </th>
                  <th @click="sort('what')">What <i v-if="currentSort === 'what'"
                                                    v-bind:class="sortIconClass"></i>
                  </th>
                  <th @click="sort('created')">When <i v-if="currentSort === 'created'"
                                                       v-bind:class="sortIconClass"></i>
                  </th>
                  <th @click="sort('due_date')">Due <i v-if="currentSort === 'due_date'"
                                                       v-bind:class="sortIconClass"></i>
                  </th>
                  <th></th>
                </tr>
                </thead>
                <transition-group name="debt-list" tag="tbody">
                  <tr v-for="(item, idx) in sortedItems" :key="idx" :class="overdueClass(item)">
                    <td>{{item.kind | titleCase}}</td>
                    <td>{{item.who}}</td>
                    <td>{{item.what}}</td>
                    <td>{{item.created | humanize}}</td>
                    <td>{{item.due_date}}</td>
                    <td>
                      <button v-if="!item.resolved" class="btn btn-sm" @click="resolve(item)">resolve</button>
                      <span v-else class="label label-success">resolved</span>
                    </td>
                  </tr>
                </transition-group>
              </table>
            </div>
            <div class="show-sm">
              <table class="table">
                <tbody>
                <tr v-for="(item, idx) in sortedItems" :key="idx" :class="overdueClass(item)">
                  <td>
                    <div class="mobile-table-td">
                      <b>{{item.what}}</b> <br>
                      {{item.kind}} to {{item.who}} <br>
                      due {{item.due_date}}
                    </div>
                  </td>
                  <td>
                    <button class="btn btn-sm" @click="resolve(item)">resolve</button>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-else class="layered-paper" key="no-debts">
            <NavGroup active-el="ledger"/>
            <h3>You are debt free.</h3>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
  import NavGroup from './NavGroup'
  import {resolveItem} from '@/api'
  import {dateToStr} from '@/utils'

  export default {
    name: "DebtItem",
    components: {
      NavGroup
    },
    data() {
      return {
        currentSort: 'due_date',
        currentSortDir: 'asc',
      };
    },
    filters: {
      humanize: (value) => {
        return dateToStr(value);
      },
      titleCase: (value) => {
        return value.replace(/(^|\s)\S/g, function (t) {
          return t.toUpperCase()
        });
      }
    },
    computed: {
      sortIconClass: function () {
        const asc = this.currentSortDir === 'asc';
        return {
          icon: true,
          'icon-arrow-down': !asc,
          'icon-arrow-up': asc,
        }
      },
      items: function () {
        return this.$store.state.items;
      },
      sortedItems: function () {
        let items = this.$store.state.items;
        return items.sort((a, b) => {
          let modifier = 1;
          if (this.currentSortDir === 'desc') modifier = -1;
          if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
          if (a[this.currentSort] > b[this.currentSort]) return modifier;
          return 0;
        });
      },
      authenticated: function () {
        return this.$store.getters.isAuthenticated()
      }
    },
    methods: {
      today: function () {
        let date = new Date();
        date.setDate(date.getDate() + 1);
        return dateToStr(date);
      },
      sort: function (column) {
        if (column === this.currentSort) {
          this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
        }
        this.currentSort = column;
      },
      resolve: function (item) {
        if (!this.authenticated) {
          this.$store.dispatch('logout');
          this.$router.replace({name: "Login"});
          return
        }
        resolveItem(item.id, this.$store.state.jwt)
            .then(() => {
              this.$store.dispatch('loadItems');
            })
            .catch(error => {
              console.log("There was error on resolving: ", error);
              if (error.response.status === 403) {
                this.$store.dispatch('logout');
                this.$router.replace({name: "Login"});
              }
            })
      },
      overdueClass: function (item) {
        let result = [];
        if (new Date(item.due_date) < new Date() && !item.resolved) {
          result.push('text-error')
        }
        return result;
      }
    },
    beforeCreate: function () {
      this.$store.dispatch('loadItems');
    }
  }
</script>

<style lang="scss" scoped>
  .debt-items {
    table {
      margin: 0 auto;
    }
  }

  .filters {
    display: block;
  }

  td, th {
    padding: 5px;
  }

  th {
    cursor: pointer;

    i {
      margin-bottom: 4px;
    }
  }

  .layered-paper {
    padding: 2em 3px;
    @media screen and (min-width: 605px) {
      padding-right: 20px;
      padding-left: 20px;
    }
    background: white;
    box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15), /* The top layer shadow */
    0 10px 0 -5px white, /* The second layer */
    0 10px 1px -4px rgba(0, 0, 0, 0.15), /* The second layer shadow */
    0 20px 0 -10px white, /* The third layer */
    0 20px 1px -9px rgba(0, 0, 0, 0.15); /* The third layer shadow */
  }

  .input-group {
    margin-bottom: 2px;
  }

  .mobile-table-td {
    text-align: left;
  }

  .debt-list-enter-active, .debt-list-leave-active {
    transition: all 800ms;
  }

  .debt-list-enter, .debt-list-leave-to /* .list-leave-active below version 2.1.8 */
  {
    opacity: 0;
    /*transform: translateY(10px);*/
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .2s ease-in-out;
  }

  .fade-enter, .fade-leave-to {
    opacity: 0
  }
</style>
