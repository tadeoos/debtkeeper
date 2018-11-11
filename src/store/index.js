import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        items: [{
                what: 'Alice in Wonderland',
                due: '2018-12-06',
                kind: 'Debt',
                who: 'Marcin',
                created: new Date(2018, 9, 12, 16, 20, 12),
            },
            {
                what: 'Ulysses',
                due: '2018-12-23',
                kind: 'Loan',
                who: 'Iwonka',
                created: new Date(2018, 8, 12, 16, 20, 12),
            },
        ]
    },
    mutations: {
        addItem(state, item) {
            state.items.push(item);
        },
        resolveItem(state, item) {
            state.items = state.items.filter(el => el !== item);
        }
    },
    actions: {
        // getParts({commit}) {
        //     axios.get('/api/parts')
        //         .then(result => commit('updateParts', result.data))
        //         .catch(console.error);
        // },
        // addItem({commit, state}, robot) {
        //     const items = [...state.items, item];
        //     return axios.post('/api/cart', cart)
        //         .then(() => commit('addRobotToCart', robot));
        // },
    },
    getters: {},
});
