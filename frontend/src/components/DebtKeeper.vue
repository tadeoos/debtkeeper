<template>
  <div class="container">
    <div class="columns">
      <div class="debt-form column col-lg-12 col-4 col-mx-auto">
        <form>
          <div class="input-group">
            <label class="form-radio">
              <input type="radio" name="kind" value="Debt" v-model="kind">
              <i class="form-icon"></i> Debt
            </label>
            <label class="form-radio">
              <input type="radio" name="kind" value="Loan" checked v-model="kind">
              <i class="form-icon"></i> Loan
            </label>
          </div>
          <div class="input-group" v-bind:class="{ 'has-error': whoError }">
            <span class="input-group-addon">Who</span>
            <input class="form-input" type="text" id="who" placeholder="James" v-model="who">
          </div>
          <div class="input-group" v-bind:class="{ 'has-error': whatError }">
            <span class="input-group-addon">What</span>
            <input class="form-input" type="text" id="what" placeholder="Ulysses or 100$ or..."
                   v-model="what">
          </div>
          <div class="input-group" v-bind:class="{ 'has-error': dueError }">
            <span class="input-group-addon">When</span>
            <input class="form-input" id="due" type="date" v-model="due">
            <button class="btn btn-primary" @click.stop.prevent="addDebtItem">add</button>
          </div>
        </form>
      </div>
      <div class="debt-items column col-lg-12 col-6 col-mx-auto">
        <transition name="fade" mode="out-in">
          <div class="layered-paper" v-if="items.length" key="debts-exists">
            <h5>LEDGER</h5>
            <div class="hide-sm">
              <table class="table table-striped">
                <thead>
                <tr>
                  <th @click="sort('kind')">Kind <i v-if="currentSort === 'kind'"
                                                    v-bind:class="sortIconClass"></i>
                  </th>
                  <th @click="sort('who')">Who <i v-if="currentSort === 'who'"
                                                  v-bind:class="sortIconClass"></i>
                  </th>
                  <th @click="sort('what')">What <i v-if="currentSort === 'what'"
                                                    v-bind:class="sortIconClass"></i>
                  </th>
                  <th @click="sort('due_date')">Due <i v-if="currentSort === 'due_date'"
                                                  v-bind:class="sortIconClass"></i>
                  </th>
                  <th @click="sort('created')">Created <i v-if="currentSort === 'created'"
                                                          v-bind:class="sortIconClass"></i></th>
                  <th></th>
                </tr>
                </thead>
                <transition-group name="debt-list" tag="tbody">
                  <tr v-for="(item, idx) in sortedItems" :key="idx">
                    <td>{{item.kind}}</td>
                    <td>{{item.who}}</td>
                    <td>{{item.what}}</td>
                    <td>{{item.due_date}}</td>
                    <td>{{item.created | humanize}}</td>
                    <td>
                      <button class="btn btn-sm" @click="resolve(item)">resolve</button>
                    </td>
                  </tr>
                </transition-group>
              </table>
            </div>
            <div class="show-sm">
              <table class="table">
                <tbody>
                <tr v-for="(item, idx) in sortedItems" :key="idx">
                  <td>
                    <div class="mobile-table-td">
                      <b>{{item.what}}</b> <br>
                      {{item.kind}} to {{item.who}} <br>
                      due {{item.due}}
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
            <h3>You are debt free.</h3>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
  import {postNewItem} from '@/api'

  function dateToStr(date) {
    function pad(n) {
      return n < 10 ? '0' + n : n
    }
    var date = new Date(date);
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`
  }

  export default {
    name: "DebtItem",
    data() {
      return {
        currentSort: 'due',
        currentSortDir: 'asc',
        what: '',
        due: this.today(),
        kind: 'Debt',
        who: '',
        whatError: false,
        whoError: false,
        dueError: false,
      };
    },
    filters: {
      humanize: function (value) {
        return dateToStr(value);
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
    },
    methods: {
      today: function () {
        let date = new Date();
        date.setDate(date.getDate() + 1);
        return dateToStr(date);
      },
      addDebtItem: function () {
        this.dueError = new Date(this.due) < new Date();
        this.whoError = !this.who;
        this.whatError = !this.what;
        if (this.dueError || this.whoError || this.whatError) return;

        const item = {
          what: this.what,
          due_date: this.due,
          kind: this.kind,
          who: this.who,
          user: this.$store.state.userId
        };

        postNewItem(item)
            .then((response) => {
              this.$store.dispatch('loadItems');
            });

        this.what = '';
        this.who = '';
        this.kind = 'Debt';
        this.due = this.today();
      },
      sort: function (column) {
        //if column == current sort, reverse
        if (column === this.currentSort) {
          this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
        }
        this.currentSort = column;
      },
      resolve: function (item) {
        this.$store.commit('resolveItem', item);
      }
    },
    mounted: function () {
      this.$store.dispatch('loadItems');
    }
  }
</script>

<style lang="scss" scoped>
  .debt-form {
    padding-top: 2em;
    padding-bottom: 2em;
  }
  .debt-items {
    padding-top: 2em;
    margin: 0 auto;
  }
  .debt-items {
    table {
      margin: 0 auto;
    }
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
    padding: 20px 3px;
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
