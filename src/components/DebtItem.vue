<template>
    <div class="container columns">
        <div class="debt-form column col-md-12 col-4 col-ml-auto">
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
                    <!--<p v-if="whoError" class="form-input-hint">This field can't be empty</p>-->
                </div>
                <div class="input-group" v-bind:class="{ 'has-error': whatError }">
                    <span class="input-group-addon">What</span>
                    <input class="form-input" type="text" id="what" placeholder="Ulysses or 100$ or..." v-model="what">
                    <!--<p v-if="whatError" class="form-input-hint">This field can't be empty</p>-->
                </div>
                <div class="input-group" v-bind:class="{ 'has-error': dueError }">
                    <span class="input-group-addon">When</span>
                    <input class="form-input" id="due" type="date" v-model="due">
                    <!--<p v-if="dueError" class="form-input-hint">Due date must be in the future.</p>-->
                    <button class="btn btn-primary" @click.stop.prevent="addDebtItem">add</button>
                </div>

                <!--<div class="input-group">-->
                    <!--<span class="input-group-addon">Kind</span>-->
                    <!--<select class="form-select" v-model="kind">-->
                        <!--<option>Loan</option>-->
                        <!--<option>Debt</option>-->
                    <!--</select>-->
                    <!--<button class="btn btn-primary input-group-btn" @click.stop.prevent="addDebtItem">add</button>-->
                <!--</div>-->
            </form>
        </div>
        <div class="debt-items column col-md-12 col-6 col-mr-auto layered-paper">
            <h5>LEDGER</h5>
            <table>
                <thead>
                <tr>
                    <th @click="sort('kind')">Kind <i v-if="currentSort === 'kind'" v-bind:class="sortIconClass"></i></th>
                    <th @click="sort('who')">Who <i v-if="currentSort === 'who'" v-bind:class="sortIconClass"></i></th>
                    <th @click="sort('what')">What <i v-if="currentSort === 'what'" v-bind:class="sortIconClass"></i></th>
                    <th @click="sort('due')">Due <i v-if="currentSort === 'due'" v-bind:class="sortIconClass"></i></th>
                    <th @click="sort('created')">Created <i v-if="currentSort === 'created'" v-bind:class="sortIconClass"></i></th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(item, idx) in sortedItems" :key="idx">
                    <td>{{item.kind}}</td>
                    <td>{{item.who}}</td>
                    <td>{{item.what}}</td>
                    <td>{{item.due}}</td>
                    <td>{{item.created | humanize}}</td>
                    <td>
                        <button class="btn btn-sm" @click="resolve(item)">resolve</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    function dateToStr(date) {
        return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
    }
    export default {
        name: "DebtItem",
        data() {
            return {
                currentSort: 'created',
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
        methods:{
            today: function() {
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
                    due: this.due,
                    kind: this.kind,
                    who: this.who,
                    created: new Date(),
                };
                this.$store.commit('addItem', item);

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
        }
    }
</script>

<style scoped>
    .debt-form {
        padding-top: 2em;
    }
    .debt-form form {
        /*margin: 0 0;*/
        margin-right: 0;
        margin-left: auto;
        max-width: 400px;
    }
    .debt-items {
        padding-top: 2em;
        /*margin-top: 2em;*/
        margin-left: 2em;
    }
    .debt-items table {
        margin: 0 auto;
    }
    td, th {
        padding: 5px;
    }
    th {
        cursor: pointer;
    }
    th i {
        margin-bottom: 4px;
    }
    .layered-paper {
        background: white;
        box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15), /* The top layer shadow */ 0 10px 0 -5px white, /* The second layer */ 0 10px 1px -4px rgba(0, 0, 0, 0.15), /* The second layer shadow */ 0 20px 0 -10px white, /* The third layer */ 0 20px 1px -9px rgba(0, 0, 0, 0.15); /* The third layer shadow */
    }
    .input-group {
        margin-bottom: 2px;
    }
</style>
