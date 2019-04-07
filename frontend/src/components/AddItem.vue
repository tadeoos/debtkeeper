<template>
  <div class="container">
    <div class="columns">
      <div class="debt-form column col-lg-12 col-4 col-mx-auto">
        <NavGroup active-el="add"/>
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
    </div>
  </div>
</template>

<script>
  import NavGroup from './NavGroup'
  import {postNewItem} from '@/api'

  export default {
    name: "AddItem",
    components: {
      NavGroup
    },
    data() {
      return {
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
    // computed: {
    //   sortIconClass: function () {
    //     const asc = this.currentSortDir === 'asc';
    //     return {
    //       icon: true,
    //       'icon-arrow-down': !asc,
    //       'icon-arrow-up': asc,
    //     }
    //   },
    //   items: function () {
    //     return this.$store.state.items;
    //   },
    //   sortedItems: function () {
    //     let items = this.$store.state.items;
    //     return items.sort((a, b) => {
    //       let modifier = 1;
    //       if (this.currentSortDir === 'desc') modifier = -1;
    //       if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
    //       if (a[this.currentSort] > b[this.currentSort]) return modifier;
    //       return 0;
    //     });
    //   },
    // },
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
    },
  }
</script>

<style lang="scss" scoped>
  .debt-form {
    padding-top: 2em;
    padding-bottom: 2em;
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

  .menu-link {
    margin-top: 1.2em;
  }

</style>
