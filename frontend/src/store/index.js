import Vue from 'vue';
import Vuex from 'vuex';
import {authenticate, register} from '@/api'
import {isValidJwt, EventBus} from '@/utils'

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
    ],
    user: {},
    jwt: ''
  },
  mutations: {
    addItem(state, item) {
      state.items.push(item);
    },
    resolveItem(state, item) {
      state.items = state.items.filter(el => el !== item);
    },
    setUserData(state, payload) {
      console.log('setUserData payload = ', payload);
      state.userData = payload.userData
    },
    setJwtToken(state, payload) {
      console.log('setJwtToken payload = ', payload);
      localStorage.token = payload.jwt.token;
      state.jwt = payload.jwt
    }
  },
  actions: {
    login(context, userData) {
      context.commit('setUserData', {userData});
      console.log('login yo')
      return authenticate(userData)
          .then(response => context.commit('setJwtToken', {jwt: response.data}))
          .catch(error => {
            console.log('Error Authenticating: ', error);
            EventBus.$emit('failedAuthentication', error)
          })
    },
    register(context, userData) {
      console.log('register yo')
      context.commit('setUserData', {userData});
      return register(userData)
          .then(context.dispatch('login', userData))
          .catch(error => {
            console.log('Error Registering: ', error);
            EventBus.$emit('failedRegistering: ', error)
          })
    },

  },
  getters: {
    isAuthenticated(state) {
      return isValidJwt(state.jwt.token)
    }
  },
});
