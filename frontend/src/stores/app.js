// Utilities
import axios from 'axios';
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    user: null,
    is_admin: false,
    invalid_login: false,
  }),

  actions: {
    async login(email, password) {
      this.invalid_login = false;
      
      const response = await axios.post('http://127.0.0.1:5000/login', { email, password });
      const { token, user, is_admin } = response.data;
      console.log('Logged in as', user);
      localStorage.setItem('token', token);
      localStorage.setItem('is_admin', is_admin);
      
      if(response.status === 401 || response.status === 404){
        this.invalid_login = true;
      }
      this.user = user;
      this.is_admin = is_admin;
    },

    async signup(email, password, username) {
      const response = await axios.post('http://127.0.0.1:5000/signup', { email, password, username });
      const { token, user, is_admin } = response.data;
      console.log('Logged in as', user);
      localStorage.setItem('token', token);
      this.user = user;
      this.is_admin = is_admin;
    },

    logout() {
      localStorage.removeItem('token');
      this.user = null;
    },
  },
})
