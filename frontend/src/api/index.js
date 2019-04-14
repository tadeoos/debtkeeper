import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL;

let config = {
  headers: {
    'Content-Type': 'application/json',
  }
};

let auth_config = {
  headers: {
    'Content-Type': 'multipart/form-data',
  }
};

function tokenHeader(jwt) {
  return {
    headers: {
      Authorization: `Bearer ${jwt}`, 'Content-Type': 'application/json'
    }
  }
}

function constructParams(params) {
  if (Object.keys(params).every(function (k) {
    return params[k]
  })) {
    return {}
  }
  let params_data = {params: {}};

  if (!params.resolved || !params.unresolved) {
    params_data.params.resolved = params.resolved
  }
  if (!params.loan || !params.debt) {
    params_data.params.kind = params.loan ? 'loan' : 'debt'
  }
  return params_data
}

export function getItems(jwt, filters) {
  let params = constructParams(filters);
  return axios.get(`${API_URL}/items`, {...tokenHeader(jwt), ...params})
}

export function postNewItem(item, jwt) {
  return axios.post(`${API_URL}/items`, item, tokenHeader(jwt))
}

export function resolveItem(itemId, jwt) {
  return axios.patch(`${API_URL}/items/${itemId}`, {'resolved': true}, tokenHeader(jwt))
}


export function authenticate(userData) {
  return axios.post(`${API_URL}/token`, userData, auth_config)
}

export function register(userData) {
  return axios.post(`${API_URL}/register`, userData, auth_config)
}

export function logout(jwt) {
  return axios.post(`${API_URL}/logout`, {}, tokenHeader(jwt))
}
