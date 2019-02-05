import Vue from 'vue';
import Router from 'vue-router';

import store from '@/store'
import DebtKeeper from '../components/DebtKeeper.vue'
import LoginPage from "../components/LoginPage";
import MainMenu from "../components/MainMenu";


Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [{
    path: '/',
    name: 'Home',
    components: {
      default: MainMenu,
    },
  }, {
    path: '/login',
    name: 'Login',
    components: {
      default: LoginPage,
    },
  },
    {
      path: '/ledger',
      name: 'Ledger',
      components: {
        default: DebtKeeper,
      },
      beforeEnter (to, from, next) {
        if (!store.getters.isAuthenticated) {
          next('/login')
        } else {
          next()
        }
      }
    }
  ],
});
