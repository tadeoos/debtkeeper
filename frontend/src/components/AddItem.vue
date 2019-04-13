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
              <input type="radio" name="kind" value="Loan" v-model="kind">
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
            <span class="input-group-addon tooltip tooltip-bottom" data-tooltip="Set a due date for this item">When</span>
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
  import {dateToStr} from '@/utils'

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

        postNewItem(item, this.$store.state.jwt)
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
  .input-group {
    margin-bottom: 2px;
  }
</style>
