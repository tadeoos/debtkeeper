import axios from 'axios';

const API_URL = 'http://127.0.0.1:5042';

function tokenHeader(jwt) {
  console.log('jwt', jwt)
  return {headers: {Authorization: `Bearer: ${jwt}`}}
}


export function getItems(jwt) {
  return axios.get(`${API_URL}/api/items`, tokenHeader(jwt))
}

export function postNewItem(item, jwt) {
  return axios.post(`${API_URL}/api/items`, item, tokenHeader(jwt))
}

let config = {
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': "*",
    }
};

export function authenticate(userData) {
  return axios.post(`${API_URL}/auth/login`, userData)
}

export function register(userData) {
  console.log(userData);
  return axios.post(`${API_URL}/auth/register`, userData, config)
}

export function logout(jwt) {
  return axios.post(`${API_URL}/auth/logout`, {}, tokenHeader(jwt))
}
