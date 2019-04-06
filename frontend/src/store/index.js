import Vue from 'vue';
import Vuex from 'vuex';
import {authenticate, register, getItems} from '@/api'
import {isValidJwt, EventBus} from '@/utils'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    items: [],
    userId: null,
    jwt: localStorage.token || ''
  },
  mutations: {
    setItems(state, payload) {
      state.items = payload.items;
    },
    setUserData(state, payload) {
      console.log('setUserData payload = ', payload);
      state.userId = payload.id.id
    },
    setJwtToken(state, payload) {
      console.log('setJwtToken payload = ', payload);
      let token = payload.jwt.token;
      localStorage.token = token;
      state.jwt = token
    }
  },
  actions: {
    login(context, userData) {
      return authenticate(userData)
          .then(response => {
            context.commit('setJwtToken', {jwt: response.data});
            context.commit('setUserData', {id: response.data});
          })
          .catch(error => {
            console.log('Error Authenticating: ', error);
            EventBus.$emit('failedAuthentication', error)
          })
    },
    register(context, userData) {
      return register(userData)
          .then(context.dispatch('login', userData))
          .catch(error => {
            console.log('Error Registering: ', error);
            EventBus.$emit('failedRegistering: ', error)
          })
    },
    loadItems(context) {
      return getItems(context.state.jwt)
          .then((response) => {
            context.commit('setItems', { items: response.data })
          })
    }
  },
  getters: {
    isAuthenticated(state) {
      return isValidJwt(state.jwt)
    }
  },
});
