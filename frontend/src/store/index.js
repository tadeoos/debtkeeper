import Vue from 'vue';
import Vuex from 'vuex';
import {authenticate, register, getItems, logout} from '@/api'
import {isValidJwt, EventBus} from '@/utils'

Vue.use(Vuex);

const tokenKey = 'token:debtkeeper';

export default new Vuex.Store({
  state: {
    items: [],
    userId: null,
    jwt: localStorage.getItem(tokenKey) || ''
  },
  mutations: {
    setItems(state, payload) {
      state.items = payload.items;
    },
    setUserData(state, payload) {
      state.userId = payload.id.id
    },
    setJwtToken(state, payload) {
      let token = payload.jwt.token;
      localStorage.setItem(tokenKey, token);
      state.jwt = token
    },
    clearToken(state) {
      localStorage.removeItem(tokenKey);
      state.jwt = '';
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
    logout(context) {
      return logout(context.state.jwt)
          .then(response => {
                context.commit('clearToken');
              })
          .catch(error => {
            console.log('Error logging out: ', error);
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
          .then(response => {
            context.commit('setItems', {items: response.data})
          })
    },
    resolveItem(context, item) {
      console.log("item resolving not implemented");
    }
  },
  getters: {
    isAuthenticated(state) {
      return isValidJwt(state.jwt)
    }
  },
});
