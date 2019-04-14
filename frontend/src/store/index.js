import Vue from 'vue';
import Vuex from 'vuex';
import {authenticate, register, getItems, logout, resolveItem} from '@/api'
import {isValidJwt, EventBus} from '@/utils'
import router from '@/router'

Vue.use(Vuex);

const tokenKey = 'token:debtkeeper';

export default new Vuex.Store({
  state: {
    items: [],
    userId: null,
    ledgerFilters: {
      'loan': true,
      'debt': true,
      'resolved': false,
      'unresolved': true
    },
    jwt: localStorage.getItem(tokenKey) || ''
  },
  mutations: {
    setItems(state, payload) {
      state.items = payload.items;
    },
    setUserData(state, payload) {
      state.userId = payload.id
    },
    setJwtToken(state, payload) {
      let token = payload.token;
      localStorage.setItem(tokenKey, token);
      state.jwt = token
    },
    clearToken(state) {
      localStorage.removeItem(tokenKey);
      state.jwt = '';
    },
    updateFilters(state, data) {
      state.ledgerFilters[data.atr] = data.val;
    }
  },
  actions: {
    login(context, userData) {
      return authenticate(userData)
          .then(response => {
            context.commit('setJwtToken', {token: response.data.access_token});
            context.commit('setUserData', {id: response.data.id});
            router.replace({name: "Ledger"});
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
          .catch(error => {
            console.log('Error Registering: ', error);
            EventBus.$emit('failedRegistering: ', error)
          })
    },
    loadItems(context) {
      return getItems(context.state.jwt, context.state.ledgerFilters)
          .then(response => {
            context.commit('setItems', {items: response.data})
          })
          .catch(error => {
            if (error.response.status === 403){
              context.commit('clearToken');
              router.replace({name: "Login"});
            }
          })
    },
    filter(context, data){
      context.commit('updateFilters', data);
      context.dispatch('loadItems');
    }
  },
  getters: {
    isAuthenticated: state => () => {
      return isValidJwt(state.jwt)
    }
  },
});
