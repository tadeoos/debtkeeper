import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

let config = {
  headers: {
    'Content-Type': 'application/json',
    // 'Access-Control-Allow-Origin': "*",
  }
};

let auth_config = {
  headers: {
    'Content-Type': 'multipart/form-data',
    // 'Access-Control-Allow-Origin': "debtkeeper"
  }
};

function tokenHeader(jwt) {
  return {headers: {
    Authorization: `Bearer ${jwt}`,
      'Content-Type': 'application/json'
  }}
}


export function getItems(jwt) {
  return axios.get(`${API_URL}/api/items`, tokenHeader(jwt))
}

export function postNewItem(item, jwt) {
  return axios.post(`${API_URL}/api/items`, item, tokenHeader(jwt))
}



export function authenticate(userData) {
  return axios.post(`${API_URL}/token`, userData, auth_config)
}

export function register(userData) {
  console.log(userData);
  return axios.post(`${API_URL}/register`, userData, auth_config)
}

export function logout(jwt) {
  return axios.post(`${API_URL}/logout`, {}, tokenHeader(jwt))
}
